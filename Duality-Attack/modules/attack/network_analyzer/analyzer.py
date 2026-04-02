#!/usr/bin/env python3
# NETWORK TRAFFIC ANALYZER - Capture dan analisis paket jaringan

import socket
import struct
import time
import threading
from collections import defaultdict
from core.colors import Colors

class NetworkTrafficAnalyzer:
    def __init__(self):
        self.name = "Network Traffic Analyzer"
        self.packet_count = 0
        self.protocols = defaultdict(int)
        self.connections = defaultdict(int)
        self.running = False
    
    def parse_ip_header(self, data):
        """Parse IP header"""
        ip_header = data[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        ttl = iph[5]
        protocol = iph[6]
        src_addr = socket.inet_ntoa(iph[8])
        dst_addr = socket.inet_ntoa(iph[9])
        
        return {
            'version': version,
            'ttl': ttl,
            'protocol': protocol,
            'src': src_addr,
            'dst': dst_addr
        }
    
    def get_protocol_name(self, protocol_num):
        """Convert protocol number to name"""
        protocols = {
            1: 'ICMP', 6: 'TCP', 17: 'UDP', 2: 'IGMP',
            89: 'OSPF', 132: 'SCTP', 41: 'IPv6'
        }
        return protocols.get(protocol_num, f'Unknown({protocol_num})')
    
    def capture_packets(self, count=50):
        """Capture network packets"""
        print(f"{Colors.CYAN}[*] Capturing {count} packets...{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}\n")
        
        try:
            # Create raw socket
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            sock.settimeout(1)
            
            captured = 0
            while captured < count and self.running:
                try:
                    packet_data, addr = sock.recvfrom(65535)
                    captured += 1
                    self.packet_count += 1
                    
                    # Parse Ethernet header
                    eth_header = packet_data[0:14]
                    eth = struct.unpack('!6s6sH', eth_header)
                    eth_protocol = socket.ntohs(eth[2])
                    
                    if eth_protocol == 8:  # IPv4
                        ip_info = self.parse_ip_header(packet_data[14:34])
                        protocol_name = self.get_protocol_name(ip_info['protocol'])
                        self.protocols[protocol_name] += 1
                        
                        print(f"{Colors.GREEN}[{captured}]{Colors.END} {ip_info['src']} → {ip_info['dst']} [{protocol_name}]")
                        
                except socket.timeout:
                    pass
                except Exception as e:
                    pass
            
            sock.close()
            
        except PermissionError:
            print(f"{Colors.RED}[!] Need root to capture packets!{Colors.END}")
            print(f"{Colors.YELLOW}[*] Run: sudo python3 duality.py{Colors.END}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Stopped by user{Colors.END}")
    
    def analyze_live(self):
        """Live traffic analysis"""
        self.running = True
        print(f"{Colors.CYAN}[*] Live traffic analysis started{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}\n")
        
        try:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            sock.settimeout(1)
            
            def print_stats():
                while self.running:
                    time.sleep(5)
                    print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
                    print(f"{Colors.BOLD}📊 TRAFFIC STATS{Colors.END}")
                    print(f"{Colors.CYAN}{'='*55}{Colors.END}")
                    print(f"{Colors.WHITE}  Total packets: {self.packet_count}{Colors.END}")
                    print(f"{Colors.WHITE}  Protocols:{Colors.END}")
                    for proto, count in sorted(self.protocols.items(), key=lambda x: -x[1])[:5]:
                        print(f"    {proto}: {count}")
            
            stats_thread = threading.Thread(target=print_stats, daemon=True)
            stats_thread.start()
            
            while self.running:
                try:
                    packet_data, addr = sock.recvfrom(65535)
                    self.packet_count += 1
                    
                    eth_header = packet_data[0:14]
                    eth = struct.unpack('!6s6sH', eth_header)
                    eth_protocol = socket.ntohs(eth[2])
                    
                    if eth_protocol == 8:  # IPv4
                        ip_info = self.parse_ip_header(packet_data[14:34])
                        protocol_name = self.get_protocol_name(ip_info['protocol'])
                        self.protocols[protocol_name] += 1
                        
                        # Simpan koneksi unik
                        conn_key = f"{ip_info['src']} → {ip_info['dst']}"
                        self.connections[conn_key] += 1
                        
                except socket.timeout:
                    pass
                except:
                    pass
            
            sock.close()
            
        except PermissionError:
            print(f"{Colors.RED}[!] Need root to capture packets!{Colors.END}")
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Colors.GREEN}[+] Analysis stopped{Colors.END}")
    
    def scan_ports(self, target, ports="1-1000"):
        """Scan ports on target"""
        print(f"{Colors.CYAN}[*] Scanning {target}...{Colors.END}")
        
        if '-' in ports:
            start, end = map(int, ports.split('-'))
            port_range = range(start, end+1)
        else:
            port_range = [int(p) for p in ports.split(',')]
        
        open_ports = []
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                print(f"{Colors.GREEN}[+] Port {port}: OPEN{Colors.END}")
            sock.close()
        
        return open_ports
    
    def run(self):
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       📡 NETWORK TRAFFIC ANALYZER{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Capture Packets (Limited)")
        print(f"{Colors.GREEN}[2]{Colors.END} Live Traffic Analysis")
        print(f"{Colors.GREEN}[3]{Colors.END} Port Scanner")
        print(f"{Colors.GREEN}[4]{Colors.END} Show Network Interfaces")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            count = int(input(f"{Colors.GREEN}Number of packets > {Colors.END}") or "50")
            self.capture_packets(count)
        
        elif choice == '2':
            self.analyze_live()
        
        elif choice == '3':
            target = input(f"{Colors.GREEN}Target IP > {Colors.END}")
            ports = input(f"{Colors.GREEN}Ports (default: 1-1000) > {Colors.END}") or "1-1000"
            self.scan_ports(target, ports)
        
        elif choice == '4':
            import subprocess
            subprocess.run(['ip', 'addr'])

if __name__ == "__main__":
    analyzer = NetworkTrafficAnalyzer()
    analyzer.run()
