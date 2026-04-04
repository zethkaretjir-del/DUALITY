#!/usr/bin/env python3
# USB CONTROL - Control USB devices
import os
import time
import json
import subprocess

class USBControl:
    def __init__(self):
        self.whitelist_file = os.path.expanduser("~/.awakened_core/usb_whitelist.json")
        self.whitelist = self.load_whitelist()
    
    def load_whitelist(self):
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_whitelist(self):
        with open(self.whitelist_file, 'w') as f:
            json.dump(self.whitelist, f, indent=2)
    
    def get_usb_devices(self):
        """Get list of USB devices"""
        devices = []
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line:
                    devices.append(line)
        except:
            pass
        return devices
    
    def add_to_whitelist(self, device_id):
        """Add USB device to whitelist"""
        if device_id not in self.whitelist:
            self.whitelist.append(device_id)
            self.save_whitelist()
            print(f"[+] Added {device_id} to whitelist")
    
    def remove_from_whitelist(self, device_id):
        """Remove USB device from whitelist"""
        if device_id in self.whitelist:
            self.whitelist.remove(device_id)
            self.save_whitelist()
            print(f"[-] Removed {device_id} from whitelist")
    
    def block_usb(self):
        """Block all USB devices"""
        try:
            os.system("echo 'blacklist usb-storage' >> /etc/modprobe.d/blacklist.conf 2>/dev/null")
            os.system("modprobe -r usb-storage 2>/dev/null")
            print("[+] USB devices blocked")
        except:
            pass
    
    def allow_usb(self):
        """Allow USB devices"""
        try:
            os.system("modprobe usb-storage 2>/dev/null")
            print("[+] USB devices allowed")
        except:
            pass
    
    def monitor(self):
        """Monitor USB insertion"""
        last_devices = set(self.get_usb_devices())
        print("[*] USB Monitor started")
        
        while True:
            current_devices = set(self.get_usb_devices())
            new_devices = current_devices - last_devices
            
            for device in new_devices:
                print(f"[!] New USB device: {device}")
                if device not in self.whitelist:
                    print(f"[!] Unauthorized USB! Blocking...")
                    self.block_usb()
            
            last_devices = current_devices
            time.sleep(2)

if __name__ == "__main__":
    usb = USBControl()
    usb.monitor()
