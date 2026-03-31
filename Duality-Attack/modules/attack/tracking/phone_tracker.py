#!/usr/bin/env python3
# PHONE TRACKER MODULE - Lacak informasi dari nomor telepon
# "Setiap nomor punya jejak"
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import json
import time
import requests
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import DATA_DIR

class PhoneTracker:
    """Track phone number information"""
    
    def __init__(self):
        self.name = "Phone Tracker"
        self.data_dir = f"{DATA_DIR}/tracking"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def clean_number(self, number):
        """Clean phone number format"""
        return number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    def track(self, number):
        """Main tracking function"""
        results = {}
        
        try:
            # Parse number
            parsed = phonenumbers.parse(number, None)
            
            # Basic info
            results['number'] = number
            results['country'] = geocoder.description_for_number(parsed, "id")
            results['provider'] = carrier.name_for_number(parsed, "id")
            results['timezone'] = list(timezone.time_zones_for_number(parsed))
            results['valid'] = phonenumbers.is_valid_number(parsed)
            results['timestamp'] = get_timestamp()
            
            # Get country code
            country_code = phonenumbers.region_code_for_number(parsed)
            results['country_code'] = country_code
            
            # Get country info from API
            try:
                resp = requests.get(f"http://ip-api.com/json/{country_code}", timeout=5)
                if resp.status_code == 200:
                    api_data = resp.json()
                    if api_data.get('status') == 'success':
                        results['continent'] = api_data.get('continent', 'N/A')
                        results['currency'] = api_data.get('currency', 'N/A')
            except:
                pass
            
            # OSINT Links
            clean = self.clean_number(number)
            results['links'] = {
                'whatsapp': f"https://wa.me/{clean}",
                'telegram': f"https://t.me/{clean}",
                'google': f"https://www.google.com/search?q={clean}",
                'truecaller': f"https://www.truecaller.com/search/{clean}"
            }
            
            return results
            
        except phonenumbers.NumberParseException as e:
            return {'error': str(e), 'number': number}
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Format: +628123456789{Colors.END}")
        
        number = input(f"{Colors.GREEN}📱 Nomor Target > {Colors.END}")
        
        print(f"\n{Colors.CYAN}[*] Melacak {number}...{Colors.END}\n")
        
        results = self.track(number)
        
        if 'error' in results:
            print(f"{Colors.RED}[!] Error: {results['error']}{Colors.END}")
            return
        
        # Display results
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📱 HASIL PELACAKAN{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}📍 Negara     :{Colors.END} {results.get('country', 'N/A')}")
        print(f"{Colors.CYAN}📡 Provider   :{Colors.END} {results.get('provider', 'N/A')}")
        print(f"{Colors.CYAN}🕐 Timezone   :{Colors.END} {', '.join(results.get('timezone', []))}")
        print(f"{Colors.CYAN}✅ Valid      :{Colors.END} {'Ya' if results.get('valid') else 'Tidak'}")
        print(f"{Colors.CYAN}🌍 Benua     :{Colors.END} {results.get('continent', 'N/A')}")
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}🔗 LINK OSINT{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        for name, link in results.get('links', {}).items():
            print(f"{Colors.CYAN}💬 {name.capitalize():10}{Colors.END}: {link}")
        
        # Save results
        filename = f"{self.data_dir}/track_{results['number'].replace('+', '')}.json"
        save_json(results, filename)
        print(f"\n{Colors.GREEN}[+] Hasil disimpan ke: {filename}{Colors.END}")

if __name__ == "__main__":
    tracker = PhoneTracker()
    tracker.run()
