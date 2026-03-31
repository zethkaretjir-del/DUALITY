#!/usr/bin/env python3
# LINK EXTRACTOR - Extract all links from website

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from core.colors import Colors

class LinkExtractor:
    def __init__(self):
        self.name = "Link Extractor"
        self.links = set()
    
    def extract(self, url, depth=1):
        print(f"{Colors.CYAN}[*] Extracting links from: {url}{Colors.END}")
        
        try:
            resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(resp.text, 'html.parser')
            base_domain = urlparse(url).netloc
            
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                parsed = urlparse(full_url)
                
                if parsed.netloc == base_domain or parsed.netloc == '':
                    self.links.add(full_url)
                    print(f"{Colors.GREEN}[+] {full_url}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
        
        return list(self.links)
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
        
        if not url:
            print(f"{Colors.RED}[!] URL required!{Colors.END}")
            return
        
        results = self.extract(url)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}🔗 LINK EXTRACTOR RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}Total links found: {len(results)}{Colors.END}\n")
        
        for link in list(results)[:50]:
            print(f"  {Colors.WHITE}• {link}{Colors.END}")

if __name__ == "__main__":
    tool = LinkExtractor()
    tool.run()
