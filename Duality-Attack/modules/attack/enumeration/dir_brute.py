#!/usr/bin/env python3
# DIRECTORY BRUTE FORCE - Find hidden directories

import requests
import threading
from core.colors import Colors

class DirBrute:
    def __init__(self):
        self.name = "Directory Brute Force"
        self.common_dirs = [
            "admin", "login", "wp-admin", "administrator", "cpanel", "phpmyadmin",
            "backup", "uploads", "images", "css", "js", "assets", "static",
            "api", "v1", "v2", "v3", "test", "dev", "staging", "old", "new",
            "config", "conf", "include", "inc", "lib", "src", "vendor"
        ]
    
    def brute(self, url, threads=20):
        found = []
        print(f"{Colors.CYAN}[*] Brute forcing: {url}{Colors.END}")
        print(f"{Colors.DIM}[*] Testing {len(self.common_dirs)} directories...{Colors.END}\n")
        
        def check(dir_name):
            test_url = f"{url.rstrip('/')}/{dir_name}"
            try:
                resp = requests.get(test_url, timeout=3)
                if resp.status_code == 200:
                    print(f"{Colors.GREEN}[+] Found: {test_url} (200){Colors.END}")
                    found.append({"url": test_url, "status": resp.status_code})
                elif resp.status_code == 403:
                    print(f"{Colors.YELLOW}[!] Forbidden: {test_url} (403){Colors.END}")
                    found.append({"url": test_url, "status": resp.status_code})
            except:
                pass
        
        thread_list = []
        for dir_name in self.common_dirs:
            t = threading.Thread(target=check, args=(dir_name,))
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
        url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
        
        if not url:
            print(f"{Colors.RED}[!] URL required!{Colors.END}")
            return
        
        results = self.brute(url)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📁 DIRECTORY BRUTE FORCE RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}Total found: {len(results)}{Colors.END}\n")
        
        for r in results:
            print(f"  {Colors.WHITE}• {r['url']} ({r['status']}){Colors.END}")

if __name__ == "__main__":
    tool = DirBrute()
    tool.run()
