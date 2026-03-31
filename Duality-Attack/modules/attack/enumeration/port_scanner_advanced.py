#!/usr/bin/env python3
# PORT SCANNER ADVANCED - Fast multi-threaded port scanner

import socket
import threading
from core.colors import Colors

class PortScannerAdvanced:
    def __init__(self):
        self.name = "Port Scanner Advanced"
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            27017: "MongoDB"
        }
    
    def scan_port(self, target, port, results):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                service = self.common_ports.get(port, "Unknown")
                results.append({"port": port, "service": service})
                print(f"{Colors.GREEN}[+] Port {port}: {service}{Colors.END}")
            sock.close()
        except:
            pass
    
    def scan(self, target, ports, threads=50):
        results = []
        print(f"{Colors.CYAN}[*] Scanning {target}{Colors.END}")
        print(f"{Colors.DIM}[*] Testing {len(ports)} ports...{Colors.END}\n")
        
        thread_list = []
        for port in ports:
            t = threading.Thread(target=self.scan_port, args=(target, port, results))
            t.start()
            thread_list.append(t)
            
            if len(thread_list) >= threads:
                for t in thread_list:
                    t.join()
                thread_list = []
        
        for t in thread_list:
            t.join()
        
        return results
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        target = input(f"{Colors.GREEN}Target IP/Domain > {Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Common ports (1-1000)")
        print(f"{Colors.GREEN}[2]{Colors.END} All ports (1-65535)")
        print(f"{Colors.GREEN}[3]{Colors.END} Custom ports")
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            ports = range(1, 1001)
        elif choice == '2':
            ports = range(1, 65536)
        elif choice == '3':
            custom = input(f"{Colors.GREEN}Ports (comma separated) > {Colors.END}")
            ports = [int(p.strip()) for p in custom.split(',')]
        else:
            return
        
        results = self.scan(target, ports)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}🔌 PORT SCAN RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.CYAN}Total open ports: {len(results)}{Colors.END}\n")
        
        for r in results:
            print(f"  {Colors.WHITE}• Port {r['port']}: {r['service']}{Colors.END}")

if __name__ == "__main__":
    tool = PortScannerAdvanced()
    tool.run()
