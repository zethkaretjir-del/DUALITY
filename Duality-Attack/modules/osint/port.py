#!/usr/bin/env python3
# Port Scanner Module

import socket
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import OSINT_DIR

class PortScanner:
    def __init__(self):
        self.name = "Port Scanner"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        target = input(f"{Colors.GREEN}🎯 Target IP/Domain > {Colors.END}")
        ports_input = input(f"{Colors.GREEN}🔌 Ports (1-1000 or 80,443) > {Colors.END}") or "1-1000"
        
        if '-' in ports_input:
            start, end = map(int, ports_input.split('-'))
            port_range = range(start, end+1)
        else:
            port_range = [int(p.strip()) for p in ports_input.split(',')]
        
        print(f"\n{Colors.CYAN}[*] Scanning {target}...{Colors.END}\n")
        
        open_ports = []
        total = len(port_range)
        
        for i, port in enumerate(port_range):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, port)) == 0:
                print(f"{Colors.GREEN}[+] Port {port}: OPEN{Colors.END}")
                open_ports.append(port)
            sock.close()
            
            if (i + 1) % 100 == 0:
                print(f"{Colors.DIM}[*] Progress: {i+1}/{total}{Colors.END}")
        
        result = {"target": target, "open_ports": open_ports, "timestamp": get_timestamp()}
        filename = f"{OSINT_DIR}/ports_{target}.json"
        save_json(result, filename)
        print(f"\n{Colors.GREEN}[+] Found {len(open_ports)} open ports. Saved to {filename}{Colors.END}")
