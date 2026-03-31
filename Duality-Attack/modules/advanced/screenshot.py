#!/usr/bin/env python3
# Screenshot Capture Module

import os
import time
from core.colors import Colors
from config.settings import DATA_DIR

class ScreenshotModule:
    def __init__(self):
        self.name = "Screenshot Module"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        
        # Try termux-screenshot
        if os.system("which termux-screenshot > /dev/null 2>&1") == 0:
            filename = f"{DATA_DIR}/screenshot_{int(time.time())}.png"
            os.system(f"termux-screenshot {filename}")
            print(f"{Colors.GREEN}[+] Screenshot saved: {filename}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] termux-screenshot not available{Colors.END}")
