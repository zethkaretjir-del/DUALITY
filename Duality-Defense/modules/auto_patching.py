#!/usr/bin/env python3
# AUTO PATCHING - Auto update and patch vulnerabilities
import os
import subprocess
import time
from datetime import datetime

class AutoPatching:
    def __init__(self):
        self.backup_dir = os.path.expanduser("~/.awakened_core/backups")
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_before_patch(self):
        """Backup before patching"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{self.backup_dir}/pre_patch_{timestamp}.tar.gz"
        os.system(f"tar -czf {backup_file} /etc /var/lib/dpkg 2>/dev/null")
        return backup_file
    
    def check_updates(self):
        """Check available updates"""
        try:
            subprocess.run(['apt', 'update'], capture_output=True, timeout=60)
            result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True, timeout=30)
            updates = [l for l in result.stdout.split('\n') if 'upgradable' in l]
            return updates
        except:
            return []
    
    def apply_updates(self):
        """Apply security updates"""
        print("[*] Checking for updates...")
        updates = self.check_updates()
        
        if not updates:
            print("[+] No updates available")
            return {"success": True, "updates": 0}
        
        print(f"[*] Found {len(updates)} updates")
        
        # Backup first
        backup = self.backup_before_patch()
        print(f"[*] Backup created: {backup}")
        
        try:
            # Apply updates
            subprocess.run(['apt', 'upgrade', '-y', '--only-upgrade'], timeout=300)
            print(f"[+] Applied {len(updates)} updates")
            return {"success": True, "updates": len(updates), "backup": backup}
        except Exception as e:
            print(f"[!] Update failed: {e}")
            # Restore if failed
            os.system(f"tar -xzf {backup} -C / 2>/dev/null")
            return {"success": False, "error": str(e)}
    
    def schedule_daily(self):
        """Schedule daily updates"""
        cron_line = f"0 2 * * * python3 {__file__} --auto\n"
        try:
            subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -', shell=True)
            print("[+] Daily updates scheduled at 2 AM")
        except:
            print("[!] Failed to schedule updates")

if __name__ == "__main__":
    import sys
    patcher = AutoPatching()
    
    if '--auto' in sys.argv:
        patcher.apply_updates()
    else:
        patcher.apply_updates()
        patcher.schedule_daily()
