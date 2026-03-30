#!/usr/bin/env python3
# VPN MONITOR - Monitor VPN connection, kill switch
import os
import time
import subprocess
import threading

class VPNMonitor:
    def __init__(self):
        self.vpn_interface = "tun0"
        self.running = False
        self.kill_switch_active = False
    
    def check_vpn(self):
        """Check if VPN is connected"""
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        return self.vpn_interface in result.stdout
    
    def enable_kill_switch(self):
        """Block all non-VPN traffic"""
        if not self.kill_switch_active:
            os.system("iptables -P OUTPUT DROP 2>/dev/null")
            os.system(f"iptables -A OUTPUT -o {self.vpn_interface} -j ACCEPT 2>/dev/null")
            self.kill_switch_active = True
            print("[+] Kill switch enabled")
    
    def disable_kill_switch(self):
        """Disable kill switch"""
        if self.kill_switch_active:
            os.system("iptables -P OUTPUT ACCEPT 2>/dev/null")
            os.system(f"iptables -D OUTPUT -o {self.vpn_interface} -j ACCEPT 2>/dev/null")
            self.kill_switch_active = False
            print("[-] Kill switch disabled")
    
    def monitor(self):
        """Monitor VPN connection"""
        self.running = True
        print("[*] VPN Monitor started")
        
        while self.running:
            if self.check_vpn():
                if self.kill_switch_active:
                    print("[+] VPN reconnected, kill switch disabled")
                    self.disable_kill_switch()
            else:
                if not self.kill_switch_active:
                    print("[!] VPN disconnected! Enabling kill switch...")
                    self.enable_kill_switch()
            time.sleep(5)
    
    def stop(self):
        self.running = False
        self.disable_kill_switch()
        print("[*] VPN Monitor stopped")

if __name__ == "__main__":
    vpn = VPNMonitor()
    try:
        vpn.monitor()
    except KeyboardInterrupt:
        vpn.stop()
