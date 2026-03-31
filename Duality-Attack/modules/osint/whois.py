#!/usr/bin/env python3
# WHOIS Lookup Module

import whois
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class WHOISLookup:
    def __init__(self):
        self.name = "WHOIS Lookup"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        domain = input(f"{Colors.GREEN}🌐 Domain > {Colors.END}")
        
        try:
            w = whois.whois(domain)
            print(f"\n{Colors.GREEN}[+] WHOIS Results:{Colors.END}")
            print(f"  Domain: {w.domain_name}")
            print(f"  Registrar: {w.registrar}")
            print(f"  Creation: {w.creation_date}")
            print(f"  Expiration: {w.expiration_date}")
            print(f"  Name Servers: {w.name_servers}")
            
            result = {"domain": domain, "whois": str(w), "timestamp": get_timestamp()}
            filename = f"{OSINT_DIR}/whois_{domain}.json"
            save_json(result, filename)
            print(f"{Colors.GREEN}[+] Saved to {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] WHOIS failed: {e}{Colors.END}")
