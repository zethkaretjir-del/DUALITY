#!/usr/bin/env python3
# Auto Updater Module

import os
import subprocess
from core.colors import Colors

class AutoUpdater:
    def __init__(self):
        self.name = "Auto Updater"
        self.repo_url = "https://github.com/zethkaretjir-del/DUALITY.git"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Check for updates")
        print(f"{Colors.GREEN}[2] Perform update")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            print(f"{Colors.CYAN}[*] Checking for updates...{Colors.END}")
            result = subprocess.run(['git', 'fetch', 'origin'], capture_output=True, text=True)
            result2 = subprocess.run(['git', 'log', 'HEAD..origin/main', '--oneline'], capture_output=True, text=True)
            
            if result2.stdout:
                print(f"{Colors.GREEN}[+] Updates available:{Colors.END}")
                print(result2.stdout)
            else:
                print(f"{Colors.GREEN}[+] Already up to date!{Colors.END}")
        
        elif choice == '2':
            print(f"{Colors.CYAN}[*] Pulling updates...{Colors.END}")
            result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
            print(f"{Colors.GREEN}[+] Update completed!{Colors.END}")
            print(result.stdout[:500])
