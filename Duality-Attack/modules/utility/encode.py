#!/usr/bin/env python3
# Encode/Decode Module

import base64
from core.colors import Colors

class EncodeDecode:
    def __init__(self):
        self.name = "Encode/Decode"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Base64 Encode")
        print(f"{Colors.GREEN}[2] Base64 Decode")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        text = input(f"{Colors.GREEN}Text > {Colors.END}")
        
        if choice == '1':
            print(f"{Colors.GREEN}[+] {base64.b64encode(text.encode()).decode()}{Colors.END}")
        elif choice == '2':
            try:
                print(f"{Colors.GREEN}[+] {base64.b64decode(text).decode()}{Colors.END}")
            except:
                print(f"{Colors.RED}[!] Invalid Base64{Colors.END}")
