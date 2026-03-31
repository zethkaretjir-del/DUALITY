#!/usr/bin/env python3
# AUTO UPDATER - Update Forgotten Core automatically
import os
import sys
import subprocess
import shutil
import time

class AutoUpdater:
    def __init__(self, repo_url="https://github.com/zethkaretjir-del/FORGOTTEN-CORE-.git"):
        self.repo_url = repo_url
        self.update_dir = os.path.expanduser("~/FORGOTTEN-CORE-UPDATE")
        
    def check_update(self):
        """Check if update available"""
        try:
            # Get current commit
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                   capture_output=True, text=True, cwd=os.path.expanduser("~/FORGOTTEN-CORE-"))
            current = result.stdout.strip()
            
            # Get latest commit from remote
            result = subprocess.run(['git', 'ls-remote', self.repo_url, 'HEAD'],
                                   capture_output=True, text=True)
            latest = result.stdout.split()[0] if result.stdout else None
            
            if latest and latest != current:
                return {"update_available": True, "current": current[:8], "latest": latest[:8]}
        except:
            pass
        return {"update_available": False}
    
    def perform_update(self):
        """Perform the update"""
        try:
            # Backup current
            backup_dir = os.path.expanduser("~/FORGOTTEN-CORE-BACKUP")
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.copytree(os.path.expanduser("~/FORGOTTEN-CORE-"), backup_dir)
            print("[+] Backup created")
            
            # Clone fresh
            if os.path.exists(self.update_dir):
                shutil.rmtree(self.update_dir)
            subprocess.run(['git', 'clone', self.repo_url, self.update_dir], capture_output=True)
            
            # Copy new files
            for item in os.listdir(self.update_dir):
                src = os.path.join(self.update_dir, item)
                dst = os.path.join(os.path.expanduser("~/FORGOTTEN-CORE-"), item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            print("[+] Update completed!")
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def restart_app(self):
        """Restart the application"""
        print("[*] Restarting application...")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
