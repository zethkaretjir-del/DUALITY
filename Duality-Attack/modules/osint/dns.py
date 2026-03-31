#!/usr/bin/env python3
# DNS Lookup Module

import dns.resolver
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class DNSLookup:
    def __init__(self):
        self.name = "DNS Lookup"
        self.record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        domain = input(f"{Colors.GREEN}🌐 Domain > {Colors.END}")
        
        results = {}
        for rtype in self.record_types:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                results[rtype] = [str(ans) for ans in answers]
                print(f"{Colors.GREEN}[+] {rtype} Records:{Colors.END}")
                for ans in answers:
                    print(f"    {ans}")
            except:
                print(f"{Colors.DIM}[!] No {rtype} records{Colors.END}")
        
        filename = f"{OSINT_DIR}/dns_{domain}.json"
        save_json(results, filename)
        print(f"{Colors.GREEN}[+] Saved to {filename}{Colors.END}")
