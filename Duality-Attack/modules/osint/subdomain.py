#!/usr/bin/env python3
# Subdomain Scanner Module

import socket
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class SubdomainScanner:
    def __init__(self):
        self.name = "Subdomain Scanner"
        self.subdomains = [
            "www", "mail", "ftp", "blog", "dev", "test", "admin", "api", "app",
            "portal", "login", "dashboard", "cdn", "assets", "static", "docs",
            "support", "help", "status", "info", "news", "shop", "store"
        ]
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        domain = input(f"{Colors.GREEN}🌐 Domain > {Colors.END}")
        
        print(f"\n{Colors.CYAN}[*] Scanning {domain}...{Colors.END}\n")
        
        found = []
        for sub in self.subdomains:
            test = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(test)
                print(f"{Colors.GREEN}[✓] {test} -> {ip}{Colors.END}")
                found.append({"subdomain": test, "ip": ip})
            except:
                print(f"{Colors.DIM}[✗] {test}{Colors.END}")
        
        result = {"domain": domain, "found": found, "timestamp": get_timestamp()}
        filename = f"{OSINT_DIR}/subdomains_{domain}.json"
        save_json(result, filename)
        print(f"\n{Colors.GREEN}[+] Found {len(found)} subdomains. Saved to {filename}{Colors.END}")
