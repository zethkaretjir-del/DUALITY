#!/usr/bin/env python3
# File Transfer Module

import os
import base64
from core.colors import Colors
from core.utils import save_file

class FileTransfer:
    def __init__(self):
        self.name = "File Transfer"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Upload file")
        print(f"{Colors.GREEN}[2] Download file")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice == '1':
            filepath = input(f"{Colors.GREEN}File > {Colors.END}")
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    content = base64.b64encode(f.read()).decode()
                filename = os.path.basename(filepath)
                save_file(content, f"/tmp/upload_{filename}.b64")
                print(f"{Colors.GREEN}[+] File encoded to /tmp/upload_{filename}.b64{Colors.END}")
        elif choice == '2':
            url = input(f"{Colors.GREEN}URL > {Colors.END}")
            output = input(f"{Colors.GREEN}Output file > {Colors.END}")
            os.system(f"curl -o {output} {url}")
            print(f"{Colors.GREEN}[+] Downloaded to {output}{Colors.END}")
