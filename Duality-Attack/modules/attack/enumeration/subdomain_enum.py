#!/usr/bin/env python3
# SUBDOMAIN ENUMERATION - Cari subdomain tersembunyi

import requests
import threading
import time
from core.colors import Colors

class SubdomainEnum:
    def __init__(self):
        self.name = "Subdomain Enumeration"
        self.common_subdomains = [
            "www", "mail", "admin", "api", "dev", "test", "blog", "shop", "ftp", "ns1",
            "webmail", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap",
            "smtp", "pop", "ns2", "ns3", "mx", "remote", "secure", "vpn", "support",
            "portal", "dashboard", "login", "auth", "account", "cdn", "static",
            "assets", "docs", "wiki", "forum", "community", "news", "download"
        ]
    
    def enumerate(self, domain, threads=20):
        found = []
        print(f"{Colors.CYAN}[*] Enumerating subdomains for: {domain}{Colors.END}")
        print(f"{Colors.DIM}[*] Testing {len(self.common_subdomains)} subdomains...{Colors.END}\n")
        
        def check(sub):
            subdomain = f"{sub}.{domain}"
            try:
                resp = requests.get(f"http://{subdomain}", timeout=3)
                if resp.status_code < 400:
                    print(f"{Colors.GREEN}[+] Found: {subdomain} ({resp.status_code}){Colors.END}")
                    found.append({"subdomain": subdomain, "status": resp.status_code})
            except:
                pass
        
        # Multi-threading
        thread_list = []
        for sub in self.common_subdomains:
            t = threading.Thread(target=check, args=(sub,))
            t.start()
            thread_list.append(t)
            
            if len(thread_list) >= threads:
                for t in thread_list:
                    t.join()
                thread_list = []
        
        for t in thread_list:
            t.join()
        
        return found
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        domain = input(f"{Colors.GREEN}Domain > {Colors.END}")
        
        if not domain:
            print(f"{Colors.RED}[!] Domain required!{Colors.END}")
            return
        
        results = self.enumerate(domain)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📊 SUBDOMAIN ENUMERATION RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}Total found: {len(results)}{Colors.END}\n")
        
        for r in results:
            print(f"  {Colors.WHITE}• {r['subdomain']}{Colors.END}")

if __name__ == "__main__":
    tool = SubdomainEnum()
    tool.run()
