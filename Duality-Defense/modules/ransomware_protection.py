#!/usr/bin/env python3
# RANSOMWARE PROTECTION - Real-time file protection
import os
import time
import hashlib
import json
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RansomwareProtection:
    def __init__(self):
        self.monitored_dirs = [os.path.expanduser("~"), "/data"]
        self.file_hashes = {}
        self.suspicious_activity = []
        self.protected_extensions = ['.txt', '.doc', '.pdf', '.jpg', '.png', '.py', '.sh']
    
    def hash_file(self, filepath):
        """Calculate file hash"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return None
    
    def scan_directory(self, directory):
        """Scan directory and store hashes"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.protected_extensions):
                    filepath = os.path.join(root, file)
                    filehash = self.hash_file(filepath)
                    if filehash:
                        self.file_hashes[filepath] = filehash
    
    def check_integrity(self):
        """Check file integrity"""
        modifications = []
        for filepath, old_hash in self.file_hashes.items():
            if os.path.exists(filepath):
                new_hash = self.hash_file(filepath)
                if new_hash and new_hash != old_hash:
                    modifications.append(filepath)
                    print(f"[!] File modified: {filepath}")
            else:
                modifications.append(filepath)
                print(f"[!] File deleted: {filepath}")
        
        if len(modifications) > 100:
            print("[!!!] RANSOMWARE DETECTED! Too many file changes!")
            return True
        return False
    
    def rollback(self, backup_dir):
        """Rollback to previous state"""
        print("[*] Rolling back changes...")
        # Restore from backup
        os.system(f"cp -r {backup_dir}/* ~/ 2>/dev/null")
        print("[+] Rollback completed")

class FileHandler(FileSystemEventHandler):
    def __init__(self, protection):
        self.protection = protection
        self.change_count = 0
        self.start_time = time.time()
    
    def on_modified(self, event):
        if not event.is_directory:
            self.change_count += 1
            if time.time() - self.start_time < 60 and self.change_count > 100:
                print("[!!!] RANSOMWARE DETECTED!")
                self.protection.rollback("/backup")

if __name__ == "__main__":
    rp = RansomwareProtection()
    observer = Observer()
    handler = FileHandler(rp)
    
    for directory in rp.monitored_dirs:
        if os.path.exists(directory):
            observer.schedule(handler, directory, recursive=True)
    
    observer.start()
    print("[*] Ransomware Protection active")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
