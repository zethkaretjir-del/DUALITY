#!/usr/bin/env python3
# Password Generator Module

import random
import string
from core.colors import Colors

class PasswordGenerator:
    def __init__(self):
        self.name = "Password Generator"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        length = int(input(f"{Colors.GREEN}Length (12) > {Colors.END}") or "12")
        count = int(input(f"{Colors.GREEN}Count (5) > {Colors.END}") or "5")
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        
        print(f"\n{Colors.GREEN}[+] Generated passwords:{Colors.END}")
        for i in range(count):
            pwd = ''.join(random.choice(chars) for _ in range(length))
            print(f"  {i+1}. {pwd}")
