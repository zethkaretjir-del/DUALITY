#!/usr/bin/env python3
# DDoS Module

import threading
import time
import socket
import requests
from core.colors import Colors

class DDoSModule:
    def __init__(self):
        self.name = "DDoS Module"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Educational purposes only{Colors.END}")
        print(f"{Colors.GREEN}[1] HTTP Flood")
        print(f"{Colors.GREEN}[2] SYN Flood")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
            duration = int(input(f"{Colors.GREEN}Duration (seconds) > {Colors.END}") or 10)
            print(f"{Colors.CYAN}[*] Simulating HTTP flood for {duration} seconds{Colors.END}")
            for i in range(duration):
                print(f"{Colors.DIM}[*] Attack in progress... {i+1}/{duration}{Colors.END}")
                time.sleep(1)
            print(f"{Colors.GREEN}[+] Attack simulation complete{Colors.END}")
        else:
            print(f"{Colors.CYAN}[*] SYN flood simulation{Colors.END}")
