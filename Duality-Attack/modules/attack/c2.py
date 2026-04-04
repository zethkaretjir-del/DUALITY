#!/usr/bin/env python3
# C2 Server Module

import os
from core.colors import Colors

class C2Server:
    def __init__(self):
        self.name = "C2 Server"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] HTTP Server (python)")
        print(f"{Colors.GREEN}[2] Netcat Listener")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            port = input(f"{Colors.GREEN}Port (80) > {Colors.END}") or "80"
            print(f"{Colors.CYAN}[*] Starting HTTP server on port {port}{Colors.END}")
            os.system(f"python3 -m http.server {port}")
        elif choice == '2':
            port = input(f"{Colors.GREEN}Port (4444) > {Colors.END}") or "4444"
            print(f"{Colors.CYAN}[*] Starting netcat listener on port {port}{Colors.END}")
            os.system(f"nc -lvnp {port}")
