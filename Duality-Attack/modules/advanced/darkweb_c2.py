#!/usr/bin/env python3
# Dark Web C2 Module (Tor Hidden Service)

import os
import subprocess
import time
from core.colors import Colors

class DarkWebC2:
    def __init__(self):
        self.name = "Dark Web C2"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Requires Tor installed{Colors.END}")
        
        print(f"{Colors.GREEN}[1] Install Tor")
        print(f"{Colors.GREEN}[2] Setup Hidden Service")
        print(f"{Colors.GREEN}[3] Get Onion URL")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            if os.system("which tor > /dev/null 2>&1") != 0:
                os.system("pkg install tor -y")
                print(f"{Colors.GREEN}[+] Tor installed{Colors.END}")
            else:
                print(f"{Colors.GREEN}[+] Tor already installed{Colors.END}")
        
        elif choice == '2':
            hidden_dir = os.path.expanduser("~/.tor/hidden_service")
            os.makedirs(hidden_dir, exist_ok=True)
            
            torrc = f"""
HiddenServiceDir {hidden_dir}
HiddenServicePort 80 127.0.0.1:5000
"""
            with open(os.path.expanduser("~/.tor/torrc"), 'w') as f:
                f.write(torrc)
            
            os.system("tor -f ~/.tor/torrc &")
            time.sleep(5)
            print(f"{Colors.GREEN}[+] Hidden service setup complete{Colors.END}")
        
        elif choice == '3':
            hostname = os.path.expanduser("~/.tor/hidden_service/hostname")
            if os.path.exists(hostname):
                with open(hostname, 'r') as f:
                    onion = f.read().strip()
                print(f"{Colors.GREEN}[+] Onion URL: http://{onion}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Hidden service not running{Colors.END}")
