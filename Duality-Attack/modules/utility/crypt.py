#!/usr/bin/env python3
# File Encryption Module

import os
from core.colors import Colors

class FileCrypt:
    def __init__(self):
        self.name = "File Crypt"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Requires: pip install cryptography{Colors.END}")
        print(f"{Colors.GREEN}[1] Encrypt file")
        print(f"{Colors.GREEN}[2] Decrypt file")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        filepath = input(f"{Colors.GREEN}File > {Colors.END}")
        
        if os.path.exists(filepath):
            print(f"{Colors.CYAN}[*] Simulating {choice} on {filepath}{Colors.END}")
            print(f"{Colors.GREEN}[+] Operation complete{Colors.END}")
        else:
            print(f"{Colors.RED}[!] File not found{Colors.END}")
