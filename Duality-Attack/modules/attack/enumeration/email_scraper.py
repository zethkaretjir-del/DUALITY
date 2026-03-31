#!/usr/bin/env python3
# EMAIL SCRAPER - Extract email addresses from website

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from core.colors import Colors

class EmailScraper:
    def __init__(self):
        self.name = "Email Scraper"
        self.emails = set()
    
    def scrape(self, url, depth=1):
        print(f"{Colors.CYAN}[*] Scraping: {url}{Colors.END}")
        
        try:
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find emails in page
            text = soup.get_text()
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            found_emails = re.findall(email_pattern, text)
            self.emails.update(found_emails)
            
            for email in found_emails:
                print(f"{Colors.GREEN}[+] Found: {email}{Colors.END}")
            
            # Find links for depth
            if depth > 1:
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    if urlparse(full_url).netloc == urlparse(url).netloc:
                        self.scrape(full_url, depth-1)
                        
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
        
        return list(self.emails)
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
        depth = input(f"{Colors.GREEN}Depth (1-3, default 1) > {Colors.END}") or "1"
        
        if not url:
            print(f"{Colors.RED}[!] URL required!{Colors.END}")
            return
        
        results = self.scrape(url, int(depth))
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📧 EMAIL SCRAPER RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}Total emails found: {len(results)}{Colors.END}\n")
        
        for email in results:
            print(f"  {Colors.WHITE}• {email}{Colors.END}")

if __name__ == "__main__":
    tool = EmailScraper()
    tool.run()
