#!/usr/bin/env python3
# Hash Generator Module

import hashlib
from core.colors import Colors

class HashGenerator:
    def __init__(self):
        self.name = "Hash Generator"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        text = input(f"{Colors.GREEN}Text > {Colors.END}")
        
        print(f"\n{Colors.GREEN}[+] Hashes:{Colors.END}")
        print(f"  MD5    : {hashlib.md5(text.encode()).hexdigest()}")
        print(f"  SHA1   : {hashlib.sha1(text.encode()).hexdigest()}")
        print(f"  SHA256 : {hashlib.sha256(text.encode()).hexdigest()}")
