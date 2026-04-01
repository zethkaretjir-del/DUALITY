#!/usr/bin/env python3
# Utility functions

import os
import sys
import time
import json
import subprocess
import random
from datetime import datetime
from .colors import Colors

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

def print_error(msg, show_tip=True):
    """Print error message dengan format keren"""
    print(f"\n{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  ❌ ERROR: {msg}{Colors.END}")
    
    if show_tip:
        tips = [
            "Type 'help' to see available commands",
            "Check your spelling",
            "Make sure you're in the right directory",
            "Run with: python3 duality.py"
        ]
        import random
        tip = random.choice(tips)
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║  💡 TIP: {tip}{Colors.END}")
    
    print(f"{Colors.RED}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.END}")

def print_warning(msg):
    """Print warning message"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  WARNING: {msg}{Colors.END}")

def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {msg}{Colors.END}")

def print_info(msg):
    """Print info message"""
    print(f"{Colors.CYAN}[*] {msg}{Colors.END}")

def loading_animation(message, duration=2, style="spinner"):
    """
    Loading animation keren
    style: "spinner", "bar", "dots", "matrix"
    """
    import time
    import sys
    
    if style == "spinner":
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        print(f"{Colors.CYAN}", end="")
        for i in range(duration * 10):
            print(f"\r{message} {spinner[i % len(spinner)]}", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{message} ✅ Done!{Colors.END}")
    
    elif style == "bar":
        width = 40
        steps = duration * 20  # lebih banyak step (20 per detik)
        print(f"{Colors.CYAN}", end="")
        for i in range(steps + 1):
            percent = i / steps
            filled = int(width * percent)
            bar = '█' * filled + '░' * (width - filled)
            print(f"\r{message} [{bar}] {percent*100:.1f}%", end="", flush=True)
            time.sleep(0.05)  # update setiap 0.05 detik
        print(f"\r{message} [{bar}] 100.0% ✅{Colors.END}")
    
    elif style == "dots":
        dots = ['.  ', '.. ', '...', '   ']
        print(f"{Colors.CYAN}", end="")
        for i in range(duration * 10):
            print(f"\r{message}{dots[i % len(dots)]}", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{message} ✅{Colors.END}")
    
    elif style == "matrix":
        chars = "01"
        print(f"{Colors.GREEN}", end="")
        for i in range(duration * 10):
            line = ""
            for _ in range(20):
                line += random.choice(chars)
            print(f"\r{message} {line}", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{message} ✅{Colors.END}")

if __name__ == "__main__":
    # Testing functions
    print("Testing utils.py...")
    
    # Test timestamp
    print(f"Timestamp: {get_timestamp()}")
    
    # Test progress bar
    print("Progress bar test:")
    for i in range(0, 101, 20):
        print(f"\r{progress_bar(i, 100)}", end="")
        time.sleep(0.2)
    print()
    
    # Test IP validation
    print(f"IP 192.168.1.1 valid: {validate_ip('192.168.1.1')}")
    print(f"IP 999.999.999.999 valid: {validate_ip('999.999.999.999')}")
    
    # Test phone validation
    print(f"Phone +628123456789 valid: {validate_phone('+628123456789')}")
    print(f"Phone 123 valid: {validate_phone('123')}")
    
    print("\n✅ utils.py loaded successfully!")
