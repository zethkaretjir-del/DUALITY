#!/usr/bin/env python3
# Email OSINT Module

import dns.resolver
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class EmailOSINT:
    def __init__(self):
        self.name = "Email OSINT"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        email = input(f"{Colors.GREEN}📧 Email > {Colors.END}")
        
        if '@' not in email:
            print(f"{Colors.RED}[!] Invalid email{Colors.END}")
            return
        
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"\n{Colors.GREEN}[+] Domain: {domain}{Colors.END}")
        print(f"{Colors.GREEN}[+] Username: {username}{Colors.END}")
        
        # MX Records
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            print(f"{Colors.CYAN}[*] MX Records:{Colors.END}")
            for record in mx:
                print(f"    {record.exchange}")
        except:
            pass
        
        result = {"email": email, "domain": domain, "username": username, "timestamp": get_timestamp()}
        filename = f"{OSINT_DIR}/email_{username}.json"
        save_json(result, filename)
        print(f"{Colors.GREEN}[+] Saved to {filename}{Colors.END}")
