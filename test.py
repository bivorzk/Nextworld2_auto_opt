import pyautogui as pg
import time
import json
from datetime import datetime

# Disable fail-safe
pg.FAILSAFE = False

def record_mouse_actions(duration=10):
    """Record mouse position and clicks for specified duration"""
    print(f"Recording mouse actions for {duration} seconds...")
    print("Move your mouse and click where needed. Recording will start in 3 seconds...")
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Recording started!")
    start_time = time.time()
    actions = []
    last_position = None
    last_click_time = 0
    
    # Track mouse state
    mouse_pressed = False
    
    while time.time() - start_time < duration:
        current_pos = pg.position()
        current_time = time.time() - start_time
        
        # Record position changes
        if last_position != current_pos:
            actions.append({
                'type': 'move',
                'x': current_pos.x,
                'y': current_pos.y,
                'timestamp': current_time
            })
            last_position = current_pos
        
        # Check for mouse clicks
        try:
            # Check if mouse button is currently pressed
            if pg.mouseDown and not mouse_pressed:
                # Mouse button just pressed
                actions.append({
                    'type': 'click_down',
                    'x': current_pos.x,
                    'y': current_pos.y,
                    'timestamp': current_time,
                    'button': 'left'
                })
                mouse_pressed = True
                last_click_time = current_time
                
            elif not pg.mouseDown and mouse_pressed:
                # Mouse button just released
                actions.append({
                    'type': 'click_up',
                    'x': current_pos.x,
                    'y': current_pos.y,
                    'timestamp': current_time,
                    'button': 'left'
                })
                mouse_pressed = False
                
        except:
            # Fallback: detect clicks by monitoring position changes with small delays
            pass
        
        time.sleep(0.01)  # Small delay to avoid excessive CPU usage
    
    print("Recording finished!")
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mouse_recording_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'duration': duration,
            'total_actions': len(actions),
            'actions': actions
        }, f, indent=2)
    
    print(f"Recording saved to {filename}")
    print(f"Total actions recorded: {len(actions)}")
    
    return actions

def replay_actions(filename):
    """Replay recorded mouse actions from file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        actions = data['actions']
        print(f"Replaying {len(actions)} actions...")
        print("Starting replay in 3 seconds...")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        start_time = time.time()
        
        for action in actions:
            # Wait until the correct timestamp
            while time.time() - start_time < action['timestamp']:
                time.sleep(0.001)
            
            if action['type'] == 'move':
                pg.moveTo(action['x'], action['y'])
            elif action['type'] == 'click_down':
                pg.mouseDown(action['x'], action['y'], button=action['button'])
            elif action['type'] == 'click_up':
                pg.mouseUp(action['x'], action['y'], button=action['button'])
        
        print("Replay finished!")
        
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"Error during replay: {e}")

if __name__ == "__main__":
    # Record for 10 seconds
    actions = record_mouse_actions(10)
    
    # Ask if user wants to replay
    replay = input("\nDo you want to replay the recorded actions? (y/n): ")
    if replay.lower() == 'y':
        # Get the latest recording file
        import glob
        files = glob.glob("mouse_recording_*.json")
        if files:
            latest_file = max(files)
            replay_actions(latest_file)