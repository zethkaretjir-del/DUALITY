#!/usr/bin/env python3
# Phone OSINT Module

import re
import requests
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class PhoneOSINT:
    """Phone number OSINT with carrier detection"""
    
    def __init__(self):
        self.name = "Phone OSINT"
        self.prefixes = {
            '811': 'Telkomsel', '812': 'Telkomsel', '813': 'Telkomsel',
            '814': 'Indosat', '815': 'Indosat', '816': 'Indosat',
            '817': 'XL Axiata', '818': 'XL Axiata', '819': 'XL Axiata',
            '821': 'Telkomsel', '822': 'Telkomsel', '823': 'Telkomsel',
            '831': 'Axis', '832': 'Axis', '833': 'Axis',
            '838': 'Axis', '852': 'Telkomsel', '853': 'Telkomsel',
            '878': 'XL Axiata', '896': 'Tri', '897': 'Tri',
            '898': 'Tri', '899': 'Tri'
        }
    
    def clean_number(self, number):
        """Clean and format phone number"""
        clean = re.sub(r'[^0-9+]', '', number)
        if clean.startswith('0'):
            return '+62' + clean[1:]
        elif clean.startswith('62') and not clean.startswith('+'):
            return '+' + clean
        elif not clean.startswith('+'):
            return '+62' + clean
        return clean
    
    def get_carrier(self, number):
        """Get carrier from prefix"""
        part = number.replace('+62', '')
        prefix = part[:3] if len(part) >= 3 else part
        return self.prefixes.get(prefix, 'Unknown')
    
    def validate(self, number):
        """Validate phone number"""
        try:
            resp = requests.get(f"http://apilayer.net/api/validate?access_key=demo&number={number}", timeout=5)
            data = resp.json()
            return data.get('valid', False), data
        except:
            return False, {}
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        raw = input(f"{Colors.GREEN}📱 Number > {Colors.END}")
        
        number = self.clean_number(raw)
        carrier = self.get_carrier(number)
        valid, api_data = self.validate(number)
        
        print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}📱 PHONE OSINT RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*50}{Colors.END}")
        print(f"{Colors.CYAN}Number :{Colors.END} {number}")
        print(f"{Colors.CYAN}Carrier:{Colors.END} {carrier}")
        
        if valid and api_data:
            print(f"{Colors.CYAN}Country:{Colors.END} {api_data.get('country_name', 'N/A')}")
            print(f"{Colors.CYAN}Location:{Colors.END} {api_data.get('location', 'N/A')}")
        
        print(f"\n{Colors.YELLOW}[*] OSINT Links:{Colors.END}")
        print(f"  WhatsApp: https://wa.me/{number}")
        print(f"  Telegram: https://t.me/+{number[1:]}")
        print(f"  Google  : https://www.google.com/search?q={number}")
        
        # Save result
        result = {
            "number": number,
            "carrier": carrier,
            "timestamp": get_timestamp(),
            "api_data": api_data
        }
        filename = f"{OSINT_DIR}/phone_{number.replace('+', '')}.json"
        save_json(result, filename)
        print(f"\n{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
