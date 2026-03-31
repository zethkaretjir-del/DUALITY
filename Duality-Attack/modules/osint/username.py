#!/usr/bin/env python3
# Username OSINT Module

import requests
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class UsernameOSINT:
    def __init__(self):
        self.name = "Username OSINT"
        self.sites = {
            "Instagram": "https://instagram.com/{}",
            "Twitter": "https://twitter.com/{}",
            "GitHub": "https://github.com/{}",
            "Reddit": "https://reddit.com/user/{}",
            "TikTok": "https://tiktok.com/@{}",
            "YouTube": "https://youtube.com/@{}",
            "Telegram": "https://t.me/{}",
            "Facebook": "https://facebook.com/{}"
        }
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        username = input(f"{Colors.GREEN}👤 Username > {Colors.END}")
        
        print(f"\n{Colors.CYAN}[*] Checking {username}...{Colors.END}\n")
        
        found = []
        for site, url_template in self.sites.items():
            url = url_template.format(username)
            try:
                resp = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if resp.status_code == 200:
                    print(f"{Colors.GREEN}[✓] {site}: {url}{Colors.END}")
                    found.append(site)
                else:
                    print(f"{Colors.DIM}[✗] {site}: not found{Colors.END}")
            except:
                print(f"{Colors.DIM}[?] {site}: error{Colors.END}")
        
        result = {"username": username, "found_on": found, "timestamp": get_timestamp()}
        filename = f"{OSINT_DIR}/username_{username}.json"
        save_json(result, filename)
        print(f"\n{Colors.GREEN}[+] Found {len(found)} profiles. Saved to {filename}{Colors.END}")
