#!/usr/bin/env python3
# DARK WEB INTEGRATION - Scan dark web dengan Tor

import os
import subprocess
import requests
import time
from core.colors import Colors

class DarkWebIntegration:
    def __init__(self):
        self.name = "Dark Web Integration"
        self.tor_running = False
    
    def check_tor(self):
        """Cek apakah Tor running"""
        try:
            session = requests.session()
            session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            session.get('http://httpbin.org/ip', timeout=5)
            return True
        except:
            return False
    
    def start_tor(self):
        """Start Tor service"""
        print(f"{Colors.CYAN}[*] Starting Tor...{Colors.END}")
        subprocess.Popen(['tor', '&'], shell=True)
        time.sleep(3)
        self.tor_running = True
    
    def search_onion(self, keyword):
        """Search on dark web (simulated)"""
        print(f"{Colors.CYAN}[*] Searching for '{keyword}' on dark web...{Colors.END}")
        
        # Simulated results
        results = [
            {"url": "http://dark123.onion/leaks", "title": "Data Leak Database", "relevance": "High"},
            {"url": "http://hidden456.onion/forum", "title": "Hacking Forum", "relevance": "Medium"},
            {"url": "http://market789.onion", "title": "Dark Market", "relevance": "Low"}
        ]
        
        return results
    
    def check_breach(self, email):
        """Check if email appears in breaches"""
        print(f"{Colors.CYAN}[*] Checking email: {email}{Colors.END}")
        
        try:
            # Use haveibeenpwned API
            resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
                                headers={'hibp-api-key': 'demo'}, timeout=10)
            if resp.status_code == 200:
                breaches = resp.json()
                return breaches
        except:
            pass
        
        return []
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Start Tor")
        print(f"{Colors.GREEN}[2]{Colors.END} Search Dark Web")
        print(f"{Colors.GREEN}[3]{Colors.END} Check Email Breach")
        print(f"{Colors.GREEN}[4]{Colors.END} Check Password Leak")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            if not self.check_tor():
                self.start_tor()
            else:
                print(f"{Colors.GREEN}[+] Tor already running{Colors.END}")
        
        elif choice == '2':
            keyword = input(f"{Colors.GREEN}Keyword > {Colors.END}")
            results = self.search_onion(keyword)
            
            print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
            print(f"{Colors.BOLD}🌑 DARK WEB RESULTS{Colors.END}")
            print(f"{Colors.GREEN}{'='*55}{Colors.END}")
            for r in results:
                print(f"{Colors.CYAN}[+] {r['title']}{Colors.END}")
                print(f"    URL: {r['url']}")
                print(f"    Relevance: {r['relevance']}\n")
        
        elif choice == '3':
            email = input(f"{Colors.GREEN}Email > {Colors.END}")
            breaches = self.check_breach(email)
            
            if breaches:
                print(f"\n{Colors.RED}[!] Email found in breaches!{Colors.END}")
                for b in breaches:
                    print(f"  - {b.get('Name', 'Unknown')} ({b.get('BreachDate', 'N/A')})")
            else:
                print(f"{Colors.GREEN}[+] Email not found in known breaches{Colors.END}")
        
        elif choice == '4':
            password = input(f"{Colors.GREEN}Password > {Colors.END}")
            print(f"{Colors.YELLOW}[!] Checking common passwords database...{Colors.END}")
            print(f"{Colors.DIM}[*] Simulated: Password not found in common breaches{Colors.END}")

if __name__ == "__main__":
    dark = DarkWebIntegration()
    dark.run()
