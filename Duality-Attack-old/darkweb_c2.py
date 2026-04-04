#!/usr/bin/env python3
# DARK WEB C2 - Run C2 as Tor Hidden Service
import os
import subprocess
import time
import requests

class DarkWebC2:
    def __init__(self, port=5000):
        self.port = port
        self.hidden_service_dir = os.path.expanduser("~/.tor/hidden_service")
        
    def install_tor(self):
        """Install Tor if not present"""
        try:
            subprocess.run(['tor', '--version'], capture_output=True)
        except:
            if os.path.exists('/data/data/com.termux'):
                os.system("pkg install tor -y")
            else:
                os.system("sudo apt install tor -y")
    
    def setup_hidden_service(self):
        """Setup Tor hidden service"""
        os.makedirs(self.hidden_service_dir, exist_ok=True)
        
        torrc = f"""
HiddenServiceDir {self.hidden_service_dir}
HiddenServicePort 80 127.0.0.1:{self.port}
"""
        torrc_path = os.path.expanduser("~/.tor/torrc")
        os.makedirs(os.path.dirname(torrc_path), exist_ok=True)
        with open(torrc_path, 'w') as f:
            f.write(torrc)
        
        # Start Tor
        os.system("tor -f ~/.tor/torrc &")
        time.sleep(5)
        
        # Get onion address
        hostname_file = os.path.join(self.hidden_service_dir, "hostname")
        if os.path.exists(hostname_file):
            with open(hostname_file, 'r') as f:
                onion = f.read().strip()
            return onion
        return None
    
    def get_onion_url(self):
        """Get the onion URL"""
        hostname_file = os.path.join(self.hidden_service_dir, "hostname")
        if os.path.exists(hostname_file):
            with open(hostname_file, 'r') as f:
                return f.read().strip()
        return None
    
    def start_c2_with_tor(self):
        """Start C2 server with Tor"""
        self.install_tor()
        onion = self.setup_hidden_service()
        
        if onion:
            print(f"[+] Hidden Service: http://{onion}")
            print(f"[+] Access via Tor Browser or: torsocks curl http://{onion}")
            return onion
        return None
