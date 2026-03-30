#!/usr/bin/env python3
# CLOUD BACKUP - Backup to Google Drive/Dropbox/Mega
import os
import json
import subprocess
import time
from datetime import datetime

class CloudBackup:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.awakened_core/cloud_backup.json")
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"google_drive": None, "dropbox": None, "mega": None}
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure_google_drive(self):
        """Configure Google Drive backup"""
        print("[*] Google Drive Configuration")
        print("Install: pip install PyDrive")
        client_id = input("Client ID: ")
        client_secret = input("Client Secret: ")
        self.config["google_drive"] = {"client_id": client_id, "client_secret": client_secret}
        self.save_config()
        print("[+] Google Drive configured")
    
    def configure_dropbox(self):
        """Configure Dropbox backup"""
        print("[*] Dropbox Configuration")
        print("Install: pip install dropbox")
        token = input("Access Token: ")
        self.config["dropbox"] = {"token": token}
        self.save_config()
        print("[+] Dropbox configured")
    
    def configure_mega(self):
        """Configure Mega.nz backup"""
        print("[*] Mega.nz Configuration")
        print("Install: pip install mega.py")
        email = input("Email: ")
        password = input("Password: ")
        self.config["mega"] = {"email": email, "password": password}
        self.save_config()
        print("[+] Mega.nz configured")
    
    def backup_to_google_drive(self, filepath):
        """Backup file to Google Drive"""
        try:
            from pydrive.auth import GoogleAuth
            from pydrive.drive import GoogleDrive
            
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            
            filename = os.path.basename(filepath)
            file_drive = drive.CreateFile({'title': filename})
            file_drive.SetContentFile(filepath)
            file_drive.Upload()
            print(f"[+] Uploaded to Google Drive: {filename}")
            return True
        except Exception as e:
            print(f"[!] Google Drive backup failed: {e}")
            return False
    
    def backup_to_dropbox(self, filepath):
        """Backup file to Dropbox"""
        try:
            import dropbox
            dbx = dropbox.Dropbox(self.config["dropbox"]["token"])
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                dbx.files_upload(f.read(), f"/{filename}")
            print(f"[+] Uploaded to Dropbox: {filename}")
            return True
        except Exception as e:
            print(f"[!] Dropbox backup failed: {e}")
            return False
    
    def backup_to_mega(self, filepath):
        """Backup file to Mega.nz"""
        try:
            from mega import Mega
            mega = Mega()
            m = mega.login(self.config["mega"]["email"], self.config["mega"]["password"])
            m.upload(filepath)
            print(f"[+] Uploaded to Mega.nz: {os.path.basename(filepath)}")
            return True
        except Exception as e:
            print(f"[!] Mega.nz backup failed: {e}")
            return False
    
    def backup(self, filepath):
        """Backup file to all configured clouds"""
        results = []
        
        if self.config["google_drive"]:
            results.append(self.backup_to_google_drive(filepath))
        if self.config["dropbox"]:
            results.append(self.backup_to_dropbox(filepath))
        if self.config["mega"]:
            results.append(self.backup_to_mega(filepath))
        
        return any(results)
    
    def schedule_backup(self, filepath, interval_hours=24):
        """Schedule regular backups"""
        def backup_loop():
            while True:
                self.backup(filepath)
                time.sleep(interval_hours * 3600)
        
        import threading
        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()
        print(f"[+] Scheduled backup every {interval_hours} hours")

if __name__ == "__main__":
    cb = CloudBackup()
    cb.configure_dropbox()
    cb.backup("/path/to/important/file")
