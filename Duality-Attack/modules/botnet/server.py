#!/usr/bin/env python3
# Botnet C2 Server Module

from core.colors import Colors

class BotnetServer:
    def __init__(self):
        self.name = "Botnet C2 Server"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        port = input(f"{Colors.GREEN}Port (5000) > {Colors.END}") or "5000"
        print(f"{Colors.CYAN}[*] Starting C2 server on port {port}{Colors.END}")
        print(f"{Colors.GREEN}[+] Server would run on http://localhost:{port}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Run web_panel/app.py for full features{Colors.END}")
