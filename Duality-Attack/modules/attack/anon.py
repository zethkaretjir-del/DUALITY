#!/usr/bin/env python3
# Anonymity Module

import os
from core.colors import Colors

class AnonymityModule:
    def __init__(self):
        self.name = "Anonymity Module"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Check Current IP")
        print(f"{Colors.GREEN}[2] Check via Tor (if installed)")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            os.system("curl -s ifconfig.me")
            print()
        elif choice == '2':
            print(f"{Colors.YELLOW}[!] Install Tor: pkg install tor{Colors.END}")
