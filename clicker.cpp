#include <windows.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <string>

bool IsRunAsAdmin() {
    BOOL fRet = FALSE;
    HANDLE hToken = NULL;
    if (OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken)) {
        TOKEN_ELEVATION Elevation;
        DWORD cbSize = sizeof(TOKEN_ELEVATION);
        if (GetTokenInformation(hToken, TokenElevation, &Elevation, sizeof(Elevation), &cbSize)) {
            fRet = Elevation.TokenIsElevated;
        }
    }
    if (hToken) {
        CloseHandle(hToken);
    }
    return fRet;
}

void performClick(int x, int y) {
    std::cout << "Left clicking at (" << x << ", " << y << ")..." << std::endl;
    
    // Set cursor position
    SetCursorPos(x, y);
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    
    // Simple left click using SendInput - most reliable method
    INPUT inputs[2] = {};
    
    // Mouse down
    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    inputs[0].mi.dx = 0;
    inputs[0].mi.dy = 0;
    inputs[0].mi.dwExtraInfo = 0;
    
    // Mouse up
    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTUP;
    inputs[1].mi.dx = 0;
    inputs[1].mi.dy = 0;
    inputs[1].mi.dwExtraInfo = 0;
    
    UINT sent = SendInput(2, inputs, sizeof(INPUT));
    std::cout << "Left click completed (" << sent << " events sent)" << std::endl;
}

int main() {
    // Check admin privileges
    if (IsRunAsAdmin()) {
        std::cout << "Running as Administrator - Good!" << std::endl;
    } else {
        std::cout << "WARNING: Not running as Administrator. Some games may not respond to clicks." << std::endl;
        std::cout << "Consider running as Administrator for better compatibility." << std::endl;
    }
    
    struct ClickPoint {
        int x, y;
        std::string name;
    };
    
    ClickPoint clickPoints[] = {
        {1321, 719, "bonusz location"},  
        {1321, 748, "dagger location"}  
    };
    
    const int numClicks = sizeof(clickPoints) / sizeof(clickPoints[0]);
    const int DELAY_MS = 1200; // 1.2 seconds delay between each click -- CHANGE THIS IF YOU WANT SLOWER/FASTER 
    
    std::cout << "Starting auto-clicker..." << std::endl;
    std::cout << "Will click " << numClicks << " locations in sequence:" << std::endl;
    for (int i = 0; i < numClicks; i++) {
        std::cout << "  " << (i+1) << ". (" << clickPoints[i].x << ", " << clickPoints[i].y << ") - " << clickPoints[i].name << std::endl;
    }
    std::cout << "Screen resolution: " << GetSystemMetrics(SM_CXSCREEN) << "x" << GetSystemMetrics(SM_CYSCREEN) << std::endl;
    std::cout << "Press Ctrl+C to stop" << std::endl;
    
    // Give time to focus on target window
    std::cout << "Starting in 3 seconds..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(3000));
    
    // Main loop
    while (true) {
        // Click first coordinate
        std::cout << "=== Clicking " << clickPoints[0].name << " ===" << std::endl;
        performClick(clickPoints[0].x, clickPoints[0].y);
        std::this_thread::sleep_for(std::chrono::milliseconds(DELAY_MS));
        
        // Click second coordinate
        std::cout << "=== Clicking " << clickPoints[1].name << " ===" << std::endl;
        performClick(clickPoints[1].x, clickPoints[1].y);
        std::this_thread::sleep_for(std::chrono::milliseconds(DELAY_MS));
        
        // Sequence complete, repeat
        std::cout << "--- Sequence complete, repeating ---" << std::endl;

        if (GetAsyncKeyState(VK_ESCAPE)) {
            std::cout << "Escape key pressed. Exiting..." << std::endl;
            break;
        }
    }
    
    return 0;
}