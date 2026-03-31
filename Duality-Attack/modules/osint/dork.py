#!/usr/bin/env python3
# Google Dork Generator Module

from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class DorkGenerator:
    def __init__(self):
        self.name = "Dork Generator"
        self.dorks = {
            '1': ('Login Pages', ['inurl:login', 'inurl:admin', 'inurl:wp-admin']),
            '2': ('Sensitive Files', ['ext:conf', 'ext:config', 'ext:sql', 'ext:db']),
            '3': ('Exposed Data', ['inurl:phpinfo.php', 'intitle:"index of"']),
            '4': ('Passwords', ['ext:passwd', 'ext:pwd', 'intext:"password"']),
            '5': ('Cameras', ['inurl:view/view.shtml', 'inurl:axis-cgi/jpg'])
        }
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        for key, (name, _) in self.dorks.items():
            print(f"{Colors.GREEN}[{key}]{Colors.WHITE} {name}{Colors.END}")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Custom dork")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '0':
            dork = input(f"{Colors.GREEN}Custom dork > {Colors.END}")
            print(f"{Colors.CYAN}https://www.google.com/search?q={dork.replace(' ', '+')}{Colors.END}")
        elif choice in self.dorks:
            name, dork_list = self.dorks[choice]
            print(f"\n{Colors.GREEN}[+] {name} Dorks:{Colors.END}")
            for dork in dork_list:
                print(f"  {Colors.CYAN}{dork}{Colors.END}")
                print(f"  https://www.google.com/search?q={dork.replace(' ', '+')}\n")
        
        result = {"dorks": self.dorks, "timestamp": get_timestamp()}
        filename = f"{OSINT_DIR}/dorks.json"
        save_json(result, filename)
        print(f"{Colors.GREEN}[+] Saved to {filename}{Colors.END}")
