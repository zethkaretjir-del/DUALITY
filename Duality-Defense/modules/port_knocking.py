#!/usr/bin/env python3
# PORT KNOCKING - Hidden port access
import socket
import time
import threading
import os

class PortKnocking:
    def __init__(self):
        self.sequence = [1234, 5678, 9012]  # Default sequence
        self.current_step = 0
        self.last_knock_time = 0
        self.timeout = 10
        self.open_port = 22
        self.listening = False
    
    def set_sequence(self, ports):
        """Set custom knock sequence"""
        self.sequence = ports
        print(f"[+] Knock sequence set: {ports}")
    
    def knock_listener(self):
        """Listen for knock sequence"""
        self.listening = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 0))
        
        print(f"[*] Port knocking listener started")
        print(f"[*] Sequence: {self.sequence}")
        
        while self.listening:
            try:
                data, addr = sock.recvfrom(1024)
                port = int(data.decode())
                
                if time.time() - self.last_knock_time > self.timeout:
                    self.current_step = 0
                
                if port == self.sequence[self.current_step]:
                    self.current_step += 1
                    self.last_knock_time = time.time()
                    
                    if self.current_step == len(self.sequence):
                        print(f"[+] Valid knock from {addr[0]}")
                        self.open_firewall(addr[0])
                        self.current_step = 0
                else:
                    self.current_step = 0
            except:
                pass
    
    def open_firewall(self, ip):
        """Open firewall for IP"""
        os.system(f"iptables -A INPUT -s {ip} -j ACCEPT 2>/dev/null")
        print(f"[+] Firewall opened for {ip}")
    
    def start(self):
        """Start port knocking listener"""
        thread = threading.Thread(target=self.knock_listener, daemon=True)
        thread.start()
    
    def stop(self):
        self.listening = False

if __name__ == "__main__":
    pk = PortKnocking()
    pk.start()
    print("Port knocking active. Send UDP packets to sequence ports")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pk.stop()
