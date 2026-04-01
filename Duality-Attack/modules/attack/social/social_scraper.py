#!/usr/bin/env python3
# SOCIAL MEDIA SCRAPER - Scrape data dari sosial media
import os
import requests
import re
import json
from core.colors import Colors

class SocialMediaScraper:
    def __init__(self):
        self.name = "Social Media Scraper"
    
    def scrape_instagram(self, username):
        """Scrape Instagram profile"""
        print(f"{Colors.DIM}[*] Scraping Instagram...{Colors.END}")
        try:
            url = f"https://www.instagram.com/{username}/"
            resp = requests.get(url, timeout=10)
            
            # Extract data from page
            data = {
                "username": username,
                "url": url,
                "exists": resp.status_code == 200
            }
            
            # Try to get follower count from meta tags
            match = re.search(r'followed_by":\{"count":(\d+)', resp.text)
            if match:
                data['followers'] = match.group(1)
            
            match = re.search(r'edge_follow":\{"count":(\d+)', resp.text)
            if match:
                data['following'] = match.group(1)
            
            return data
        except:
            return {"username": username, "exists": False, "error": "Could not scrape"}
    
    def scrape_twitter(self, username):
        """Scrape Twitter profile"""
        print(f"{Colors.DIM}[*] Scraping Twitter...{Colors.END}")
        try:
            url = f"https://twitter.com/{username}"
            resp = requests.get(url, timeout=10)
            
            return {
                "username": username,
                "url": url,
                "exists": resp.status_code == 200
            }
        except:
            return {"username": username, "exists": False}
    
    def scrape_github(self, username):
        """Scrape GitHub profile"""
        print(f"{Colors.DIM}[*] Scraping GitHub...{Colors.END}")
        try:
            url = f"https://api.github.com/users/{username}"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "username": username,
                    "url": f"https://github.com/{username}",
                    "exists": True,
                    "name": data.get('name', 'N/A'),
                    "bio": data.get('bio', 'N/A'),
                    "followers": data.get('followers', 0),
                    "following": data.get('following', 0),
                    "repos": data.get('public_repos', 0)
                }
            return {"username": username, "exists": False}
        except:
            return {"username": username, "exists": False}
    
    def scrape_tiktok(self, username):
        """Scrape TikTok profile"""
        print(f"{Colors.DIM}[*] Scraping TikTok...{Colors.END}")
        try:
            url = f"https://www.tiktok.com/@{username}"
            resp = requests.get(url, timeout=10)
            
            return {
                "username": username,
                "url": url,
                "exists": resp.status_code == 200
            }
        except:
            return {"username": username, "exists": False}
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        username = input(f"{Colors.GREEN}Username > {Colors.END}")
        
        if not username:
            print(f"{Colors.RED}[!] Username required!{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}[*] Scanning username: {username}{Colors.END}\n")
        
        results = {
            "instagram": self.scrape_instagram(username),
            "twitter": self.scrape_twitter(username),
            "github": self.scrape_github(username),
            "tiktok": self.scrape_tiktok(username)
        }
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📱 SOCIAL MEDIA RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        
        for platform, data in results.items():
            status = "✅ Found" if data.get('exists') else "❌ Not found"
            status_color = Colors.GREEN if data.get('exists') else Colors.RED
            print(f"\n{Colors.CYAN}[{platform.upper()}]{Colors.END} {status_color}{status}{Colors.END}")
            print(f"  URL: {data.get('url', 'N/A')}")
            
            if platform == 'github' and data.get('exists'):
                print(f"  Name: {data.get('name', 'N/A')}")
                print(f"  Bio: {data.get('bio', 'N/A')}")
                print(f"  Followers: {data.get('followers', 0)}")
                print(f"  Repos: {data.get('repos', 0)}")
        
        # Save results
        filename = f"social_{username}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{Colors.GREEN}[+] Results saved to {filename}{Colors.END}")

if __name__ == "__main__":
    scraper = SocialMediaScraper()
    scraper.run()
