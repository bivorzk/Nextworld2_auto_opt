import json
from collections import defaultdict

def analyze_mouse_recording(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    click_events = []
    click_coordinates = set()
    
    # Extract all click events
    for action in data['actions']:
        if action['type'] in ['click_down', 'click_up']:
            click_events.append({
                'type': action['type'],
                'x': action['x'],
                'y': action['y'],
                'timestamp': action['timestamp'],
                'button': action.get('button', 'unknown')
            })
            click_coordinates.add((action['x'], action['y']))
    
    # Analyze timing patterns
    click_timings = []
    if len(click_events) > 1:
        for i in range(1, len(click_events)):
            time_diff = click_events[i]['timestamp'] - click_events[i-1]['timestamp']
            click_timings.append(time_diff)
    
    # Group click down/up pairs
    click_pairs = []
    i = 0
    while i < len(click_events) - 1:
        if (click_events[i]['type'] == 'click_down' and 
            i + 1 < len(click_events) and 
            click_events[i + 1]['type'] == 'click_up' and
            click_events[i]['x'] == click_events[i + 1]['x'] and
            click_events[i]['y'] == click_events[i + 1]['y']):
            
            duration = click_events[i + 1]['timestamp'] - click_events[i]['timestamp']
            click_pairs.append({
                'x': click_events[i]['x'],
                'y': click_events[i]['y'],
                'start_time': click_events[i]['timestamp'],
                'end_time': click_events[i + 1]['timestamp'],
                'duration': duration,
                'button': click_events[i]['button']
            })
            i += 2
        else:
            i += 1
    
    return {
        'total_actions': data['total_actions'],
        'recording_duration': data['duration'],
        'click_events': click_events,
        'unique_coordinates': sorted(list(click_coordinates)),
        'click_timings': click_timings,
        'click_pairs': click_pairs
    }

def print_analysis(analysis):
    print("=== MOUSE RECORDING ANALYSIS ===")
    print(f"Total actions in recording: {analysis['total_actions']}")
    print(f"Recording duration: {analysis['recording_duration']} seconds")
    print(f"Total click events: {len(analysis['click_events'])}")
    print(f"Unique click coordinates: {len(analysis['unique_coordinates'])}")
    
    print("\n=== ALL CLICK EVENTS ===")
    for i, event in enumerate(analysis['click_events']):
        print(f"{i+1}. {event['type']} at ({event['x']}, {event['y']}) at {event['timestamp']:.3f}s - {event['button']} button")
    
    print("\n=== UNIQUE CLICK COORDINATES ===")
    for i, coord in enumerate(analysis['unique_coordinates']):
        print(f"{i+1}. ({coord[0]}, {coord[1]})")
    
    print("\n=== CLICK PAIRS (DOWN -> UP) ===")
    for i, pair in enumerate(analysis['click_pairs']):
        print(f"{i+1}. Click at ({pair['x']}, {pair['y']}) - Duration: {pair['duration']:.3f}s - Button: {pair['button']}")
        print(f"    Start: {pair['start_time']:.3f}s, End: {pair['end_time']:.3f}s")
    
    print("\n=== TIMING PATTERNS ===")
    if analysis['click_timings']:
        print(f"Time between consecutive click events:")
        for i, timing in enumerate(analysis['click_timings']):
            print(f"  Event {i+1} to {i+2}: {timing:.3f}s")
        
        avg_timing = sum(analysis['click_timings']) / len(analysis['click_timings'])
        print(f"Average time between clicks: {avg_timing:.3f}s")
        print(f"Min time between clicks: {min(analysis['click_timings']):.3f}s")
        print(f"Max time between clicks: {max(analysis['click_timings']):.3f}s")
    
    print("\n=== IMPLEMENTATION SUMMARY ===")
    print("For your main script, you can use these coordinates and timings:")
    print("Click coordinates to implement:")
    for coord in analysis['unique_coordinates']:
        print(f"  pyautogui.click({coord[0]}, {coord[1]})")
    
    if analysis['click_pairs']:
        print(f"\nRecommended click sequence based on recording:")
        for i, pair in enumerate(analysis['click_pairs']):
            print(f"  # Click {i+1}")
            print(f"  pyautogui.click({pair['x']}, {pair['y']})")
            if i < len(analysis['click_pairs']) - 1:
                next_pair = analysis['click_pairs'][i + 1]
                wait_time = next_pair['start_time'] - pair['end_time']
                if wait_time > 0.1:  # Only suggest wait if significant
                    print(f"  time.sleep({wait_time:.2f})  # Wait before next click")

if __name__ == "__main__":
    filename = "mouse_recording_20251206_192236.json"
    analysis = analyze_mouse_recording(filename)
    print_analysis(analysis)