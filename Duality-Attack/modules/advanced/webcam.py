#!/usr/bin/env python3
# Webcam Capture Module

import os
import time
from core.colors import Colors
from config.settings import DATA_DIR

class WebcamCapture:
    def __init__(self):
        self.name = "Webcam Capture"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        
        # Try termux-camera-photo
        if os.system("which termux-camera-photo > /dev/null 2>&1") == 0:
            filename = f"{DATA_DIR}/webcam_{int(time.time())}.jpg"
            os.system(f"termux-camera-photo {filename}")
            if os.path.exists(filename):
                print(f"{Colors.GREEN}[+] Webcam photo saved: {filename}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Failed to capture webcam{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] termux-camera-photo not available{Colors.END}")
            print(f"{Colors.CYAN}[*] Install with: pkg install termux-api{Colors.END}")
