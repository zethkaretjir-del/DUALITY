#!/usr/bin/env python3
# Stealth Cleaner Module

import os
from core.colors import Colors

class StealthCleaner:
    def __init__(self):
        self.name = "Stealth Cleaner"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Wipe Bash History")
        print(f"{Colors.GREEN}[2] Clear Temp Files")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            os.system("history -c && echo > ~/.bash_history")
            print(f"{Colors.GREEN}[+] Shell history wiped{Colors.END}")
        elif choice == '2':
            os.system("rm -rf /tmp/* 2>/dev/null")
            print(f"{Colors.GREEN}[+] Temp files cleared{Colors.END}")
