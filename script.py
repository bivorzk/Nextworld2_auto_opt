import cv2
import numpy as np
import pyautogui as pg
import time
import os
import ctypes
from ctypes import wintypes

# Windows API constants
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# Get Windows API functions
user32 = ctypes.windll.user32

# Define POINT structure
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def windows_click(x, y):
    """Perform a left click using Windows API with game compatibility"""
    # Move cursor to position
    user32.SetCursorPos(x, y)
    time.sleep(0.1)
    
    # Method 1: Direct mouse events
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)  # Longer hold time for games
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    time.sleep(0.1)
    
    # Method 2: Alternative click method for stubborn games
    # Get window handle at cursor position
    point = POINT(x, y)
    hwnd = user32.WindowFromPoint(point)
    if hwnd:
        # Send WM_LBUTTONDOWN and WM_LBUTTONUP messages
        lParam = (y << 16) | x
        user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 1, lParam)
        time.sleep(0.05)
        user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lParam)

# Disable pyautogui fail-safe
pg.FAILSAFE = False
pg.PAUSE = 0.1

# -----------------------------
# Configuration
# -----------------------------
# Recorded click coordinates from mouse recording
CLICK_COORDS = [(1321, 719)]  # Click location from recording
DELAY_AFTER_CLICK = 1.1

# -----------------------------
# Main loop
# -----------------------------
while True:
    for x, y in CLICK_COORDS:
        print(f"Clicking at recorded coordinates ({x}, {y})...")
        
        # Perform click using Windows API
        windows_click(x, y)
        
        print(f"Windows API click performed at ({x}, {y})")
        time.sleep(DELAY_AFTER_CLICK)