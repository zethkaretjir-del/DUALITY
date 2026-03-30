#!/usr/bin/env python3
# HONEYPOT NETWORK - Multiple honeypot deployment
import socket
import threading
import json
import time
from datetime import datetime

class HoneypotNetwork:
    def __init__(self):
        self.honeypots = []
        self.attack_log = []
    
    def create_ssh_honeypot(self, port=22):
        """Create SSH honeypot"""
        def ssh_handler():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', port))
            server.listen(5)
            print(f"[+] SSH Honeypot running on port {port}")
            
            while True:
                client, addr = server.accept()
                self.log_attack("SSH", addr[0], addr[1])
                client.send(b"SSH-2.0-OpenSSH_8.2\r\n")
                client.close()
        
        thread = threading.Thread(target=ssh_handler, daemon=True)
        thread.start()
        self.honeypots.append(("SSH", port))
    
    def create_http_honeypot(self, port=80):
        """Create HTTP honeypot"""
        def http_handler():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', port))
            server.listen(5)
            print(f"[+] HTTP Honeypot running on port {port}")
            
            while True:
                client, addr = server.accept()
                self.log_attack("HTTP", addr[0], addr[1])
                request = client.recv(1024).decode()
                
                # Log request
                with open("honeypot_http.log", 'a') as f:
                    f.write(f"{datetime.now()}: {addr[0]} - {request}\n")
                
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Welcome</h1>"
                client.send(response.encode())
                client.close()
        
        thread = threading.Thread(target=http_handler, daemon=True)
        thread.start()
        self.honeypots.append(("HTTP", port))
    
    def create_mysql_honeypot(self, port=3306):
        """Create MySQL honeypot"""
        def mysql_handler():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', port))
            server.listen(5)
            print(f"[+] MySQL Honeypot running on port {port}")
            
            while True:
                client, addr = server.accept()
                self.log_attack("MySQL", addr[0], addr[1])
                client.send(b"MySQL server version 5.7.33\r\n")
                client.close()
        
        thread = threading.Thread(target=mysql_handler, daemon=True)
        thread.start()
        self.honeypots.append(("MySQL", port))
    
    def create_ftp_honeypot(self, port=21):
        """Create FTP honeypot"""
        def ftp_handler():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', port))
            server.listen(5)
            print(f"[+] FTP Honeypot running on port {port}")
            
            while True:
                client, addr = server.accept()
                self.log_attack("FTP", addr[0], addr[1])
                client.send(b"220 FTP Server ready\r\n")
                client.close()
        
        thread = threading.Thread(target=ftp_handler, daemon=True)
        thread.start()
        self.honeypots.append(("FTP", port))
    
    def log_attack(self, service, ip, port):
        """Log attack attempt"""
        attack = {
            "timestamp": str(datetime.now()),
            "service": service,
            "source_ip": ip,
            "source_port": port
        }
        self.attack_log.append(attack)
        print(f"[!] {service} attack from {ip}:{port}")
        
        # Save to file
        with open("honeypot_attacks.log", 'a') as f:
            f.write(f"{datetime.now()}: {service} attack from {ip}:{port}\n")
    
    def get_stats(self):
        """Get attack statistics"""
        stats = {}
        for attack in self.attack_log:
            ip = attack["source_ip"]
            stats[ip] = stats.get(ip, 0) + 1
        return stats
    
    def start_all(self):
        """Start all honeypots"""
        self.create_ssh_honeypot(2222)  # Use high port to avoid root
        self.create_http_honeypot(8080)
        self.create_ftp_honeypot(2121)
        self.create_mysql_honeypot(3307)
        print("[+] Honeypot network active!")

if __name__ == "__main__":
    hn = HoneypotNetwork()
    hn.start_all()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\nAttack stats: {hn.get_stats()}")
