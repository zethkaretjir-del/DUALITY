#!/usr/bin/env python3
# Utility functions

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from core.colors import Colors

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner(text, color=Colors.RED, width=60):
    """Print centered banner"""
    border = color + '═' * width + Colors.RESET
    print(border)
    print(color + f"{text:^{width}}" + Colors.RESET)
    print(border)

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date():
    """Get current date"""
    return datetime.now().strftime("%Y-%m-%d")

def run_command(cmd, timeout=30):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, 
                               text=True, timeout=timeout)
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Command timeout"
    except Exception as e:
        return str(e)

def save_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    return filename

def load_json(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_file(content, filename):
    """Save text content to file"""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def read_file(filename):
    """Read file content"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ""

def file_size(filepath):
    """Get file size in human readable format"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def is_root():
    """Check if running as root"""
    return os.geteuid() == 0

def get_ip():
    """Get public IP address"""
    try:
        import requests
        ip = requests.get('https://api.ipify.org', timeout=5).text
        return ip
    except:
        return "Unknown"

def validate_ip(ip):
    """Validate IP address format"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def validate_phone(number):
    """Validate phone number format"""
    import re
    clean = re.sub(r'[^0-9+]', '', number)
    return len(clean) >= 10

def progress_bar(current, total, width=50):
    """Display progress bar"""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percent*100:.1f}%"

def confirm(prompt):
    """Ask for confirmation"""
    response = input(f"{Colors.WARN}{prompt} (y/n): {Colors.RESET}")
    return response.lower() in ['y', 'yes']

def pause():
    """Pause execution"""
    input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
