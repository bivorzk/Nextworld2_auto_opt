# Nextworld2 Auto Opt

Automated tools for mouse interaction, game automation, and input analysis for Nextworld2 and similar games.

## Features
- **clicker.cpp**: Native Windows clicker (C++), simulates mouse clicks for game automation.
- **script.py**: Python script for advanced mouse clicking using Windows API.
- **script.js**: Node.js script using nut.js for image-based clicking automation.
- **test.py**: Python script to record mouse actions and save them for analysis.
- **analyze_mouse_recording.py**: Analyze recorded mouse actions from JSON files.

## Setup

### C++ Clicker
1. Compile with:
	```sh
	g++ -o clicker.exe clicker.cpp -luser32 -lgdi32 -ladvapi32
	```
2. Run as administrator for best compatibility.

### Python Scripts
Install dependencies:
```sh
pip install pyautogui opencv-python numpy
```

### Node.js Script
Install dependencies:
```sh
npm install @nut-tree/nut-js @nut-tree/template-matcher
```

## Usage

### clicker.cpp
Automates left mouse clicks at specified coordinates. Useful for games that block standard automation tools.

### script.py
Advanced mouse clicker using Windows API. Modify coordinates in the script as needed.

### script.js
Image-based click automation. Place a screenshot (e.g., `attack.png`) in the folder and update the script to match your target image.

### test.py
Records mouse movements and clicks for a set duration. Outputs a JSON log for analysis.

### analyze_mouse_recording.py
Analyzes a mouse recording JSON file, extracting click patterns and timing.

## Tips
- Make the game client window small for easier automation.
- Place items in IV inventory slots 4-2 and 4-3 for optimal script targeting.

## License
ISC