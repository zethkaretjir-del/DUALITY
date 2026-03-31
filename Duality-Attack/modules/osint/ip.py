#!/usr/bin/env python3
# IP Tracker Module

import requests
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR, IP_API

class IPTracker:
    """IP address geolocation tracker"""
    
    def __init__(self):
        self.name = "IP Tracker"
    
    def lookup(self, ip):
        """Lookup IP address"""
        try:
            resp = requests.get(f"{IP_API}/{ip}", timeout=10)
            return resp.json()
        except:
            return None
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        target = input(f"{Colors.GREEN}🌍 IP Address > {Colors.END}")
        
        data = self.lookup(target)
        
        if data and data.get('status') == 'success':
            print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.BOLD}🌍 IP GEOLOCATION{Colors.END}")
            print(f"{Colors.GREEN}{'='*50}{Colors.END}")
            print(f"{Colors.CYAN}IP      :{Colors.END} {data.get('query')}")
            print(f"{Colors.CYAN}Country :{Colors.END} {data.get('country')} ({data.get('countryCode')})")
            print(f"{Colors.CYAN}Region  :{Colors.END} {data.get('regionName')}")
            print(f"{Colors.CYAN}City    :{Colors.END} {data.get('city')}")
            print(f"{Colors.CYAN}ZIP     :{Colors.END} {data.get('zip')}")
            print(f"{Colors.CYAN}ISP     :{Colors.END} {data.get('isp')}")
            print(f"{Colors.CYAN}Lat/Lon :{Colors.END} {data.get('lat')}, {data.get('lon')}")
            
            # Google Maps link
            print(f"\n{Colors.YELLOW}[*] Maps: https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}{Colors.END}")
            
            # Save result
            filename = f"{OSINT_DIR}/ip_{target}.json"
            save_json(data, filename)
            print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
        else:
            print(f"{Colors.RED}[!] IP not found{Colors.END}")
