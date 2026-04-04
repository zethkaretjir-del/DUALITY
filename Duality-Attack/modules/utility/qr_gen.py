#!/usr/bin/env python3
# QR CODE GENERATOR - Bikin QR code dari teks/link

import os
import qrcode
from PIL import Image
from core.colors import Colors

class QRGenerator:
    def __init__(self):
        self.name = "QR Code Generator"
        self.output_dir = os.path.expanduser("~/.duality/qr_codes")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self, data, filename=None):
        """Generate QR code"""
        if filename is None:
            filename = f"qr_{int(time.time())}.png"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        
        return filepath
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Generate QR dari teks")
        print(f"{Colors.GREEN}[2]{Colors.END} Generate QR dari file")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            data = input(f"{Colors.GREEN}Text/Link > {Colors.END}")
            if not data:
                print(f"{Colors.RED}[!] Data required!{Colors.END}")
                return
            
            filename = input(f"{Colors.GREEN}Filename (default: qr_xxx.png) > {Colors.END}")
            if not filename:
                import time
                filename = f"qr_{int(time.time())}.png"
            
            filepath = self.generate(data, filename)
            print(f"\n{Colors.GREEN}[+] QR Code generated!{Colors.END}")
            print(f"{Colors.CYAN}📍 Location: {filepath}{Colors.END}")
            print(f"{Colors.CYAN}📱 Scan to view: {data[:50]}{Colors.END}")
            
            # Buka file dengan termux-open
            try:
                os.system(f"termux-open {filepath}")
            except:
                pass
        
        elif choice == '2':
            filepath = input(f"{Colors.GREEN}File to encode > {Colors.END}")
            if not os.path.exists(filepath):
                print(f"{Colors.RED}[!] File not found!{Colors.END}")
                return
            
            with open(filepath, 'r') as f:
                data = f.read()[:1000]  # Limit 1000 chars
            
            output = input(f"{Colors.GREEN}Output filename (default: qr_file.png) > {Colors.END}")
            if not output:
                output = "qr_file.png"
            
            outpath = self.generate(data, output)
            print(f"\n{Colors.GREEN}[+] QR Code generated from file!{Colors.END}")
            print(f"{Colors.CYAN}📍 Location: {outpath}{Colors.END}")

if __name__ == "__main__":
    import time
    tool = QRGenerator()
    tool.run()
