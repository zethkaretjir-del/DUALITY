#!/usr/bin/env python3
# AWAKENED CORE v1.0 - Defense & Security Toolkit
# "Guardian of the digital realm"
# Part of DUALITY Security Framework

import os
import sys
import time
import hashlib
import subprocess
import socket
import threading
import json
import platform
import psutil
from datetime import datetime

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

# Color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    PURPLE = '\033[95m'
    DARK = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AwakenedCore:
    def __init__(self):
        self.version = "1.0"
        self.name = "AWAKENED CORE"
        self.user = "guardian"
        self.host = "secure"
        self.home = os.path.expanduser("~")
        self.data_dir = f"{self.home}/.awakened_core"
        self.log_dir = f"{self.data_dir}/logs"
        self.backup_dir = f"{self.data_dir}/backups"
        self.quarantine_dir = f"{self.data_dir}/quarantine"
        
        for d in [self.data_dir, self.log_dir, self.backup_dir, self.quarantine_dir]:
            os.makedirs(d, exist_ok=True)
    
    def get_path(self):
        p = os.getcwd().replace(self.home, "~")
        return p
    
    def prompt(self):
        path = self.get_path()
        return f"{Colors.BLUE}{Colors.BOLD}┌──({Colors.GREEN}{self.user}@{Colors.CYAN}{self.host}{Colors.BLUE})-{Colors.PURPLE}[{path}]{Colors.BLUE}\n└─{Colors.WHITE}$ {Colors.END}"
    
    def clear(self):
        os.system("clear")
        self.banner()
    
    def banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║  █████╗ ██╗    ██╗ █████╗ ██╗  ██╗███████╗███╗   ██╗███████╗██████╗       ║
║ ██╔══██╗██║    ██║██╔══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝██╔══██╗      ║
║ ███████║██║ █╗ ██║███████║█████╔╝ █████╗  ██╔██╗ ██║█████╗  ██║  ██║      ║
║ ██╔══██║██║███╗██║██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║██╔══╝  ██║  ██║      ║
║ ██║  ██║╚███╔███╔╝██║  ██║██║  ██╗███████╗██║ ╚████║███████╗██████╔╝      ║
║ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═════╝       ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.GREEN}{Colors.BOLD}                    AWAKENED CORE v{self.version} - Defense Toolkit{Colors.END}
{Colors.DARK}                         "Guardian of the digital realm"{Colors.END}
        """
        print(banner)
    
    def show_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════════╗
║                         DEFENSE MENU                                                ║
╠═══════════════════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.GREEN}[01]{Colors.WHITE} firewall / fw   {Colors.DARK}» Firewall Management (iptables){Colors.END}
{Colors.GREEN}[02]{Colors.WHITE} ids / i         {Colors.DARK}» Intrusion Detection System{Colors.END}
{Colors.GREEN}[03]{Colors.WHITE} malware / m     {Colors.DARK}» Malware Scanner{Colors.END}
{Colors.GREEN}[04]{Colors.WHITE} honeypot / hp   {Colors.DARK}» Deploy Honeypot{Colors.END}
{Colors.GREEN}[05]{Colors.WHITE} backup / b      {Colors.DARK}» System Backup & Restore{Colors.END}
{Colors.GREEN}[06]{Colors.WHITE} network / n     {Colors.DARK}» Network Monitor{Colors.END}
{Colors.GREEN}[07]{Colors.WHITE} encrypt / e     {Colors.DARK}» File Encryption{Colors.END}
{Colors.GREEN}[08]{Colors.WHITE} audit / a       {Colors.DARK}» Security Audit{Colors.END}
{Colors.GREEN}[09]{Colors.WHITE} log / l         {Colors.DARK}» Log Analyzer{Colors.END}
{Colors.GREEN}[10]{Colors.WHITE} monitor / mon   {Colors.DARK}» System Monitor{Colors.END}
{Colors.GREEN}[11]{Colors.WHITE} alert / al      {Colors.DARK}» Alert Configuration{Colors.END}
{Colors.GREEN}[12]{Colors.WHITE} clean / c       {Colors.DARK}» System Cleanup{Colors.END}
{Colors.GREEN}[13]{Colors.WHITE} help / ?        {Colors.DARK}» Show help{Colors.END}
{Colors.GREEN}[00]{Colors.WHITE} exit / quit     {Colors.DARK}» Exit{Colors.END}

{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.END}
        """
        print(menu)
    
    # ==================== FIREWALL MODULE ====================
    
    def firewall_module(self):
        """Firewall Management"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    FIREWALL MANAGEMENT                              ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Show current rules")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Block IP")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Block Port")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Allow IP")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} Reset firewall")
        print(f"{Colors.GREEN}[6]{Colors.WHITE} Back")
        
        choice = input(self.prompt())
        
        if choice == '1':
            os.system("iptables -L -n -v 2>/dev/null || echo 'Run as root'")
        elif choice == '2':
            ip = input(f"{self.prompt()}IP to block > ")
            os.system(f"iptables -A INPUT -s {ip} -j DROP 2>/dev/null")
            print(f"{Colors.GREEN}[+] Blocked {ip}{Colors.END}")
        elif choice == '3':
            port = input(f"{self.prompt()}Port to block > ")
            os.system(f"iptables -A INPUT -p tcp --dport {port} -j DROP 2>/dev/null")
            print(f"{Colors.GREEN}[+] Blocked port {port}{Colors.END}")
        elif choice == '4':
            ip = input(f"{self.prompt()}IP to allow > ")
            os.system(f"iptables -A INPUT -s {ip} -j ACCEPT 2>/dev/null")
            print(f"{Colors.GREEN}[+] Allowed {ip}{Colors.END}")
        elif choice == '5':
            os.system("iptables -F 2>/dev/null")
            print(f"{Colors.GREEN}[+] Firewall reset{Colors.END}")
    
    # ==================== IDS MODULE ====================
    
    def ids_module(self):
        """Intrusion Detection System"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    INTRUSION DETECTION                             ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        suspicious_ports = [22, 23, 445, 3389, 5900, 4444, 1337, 31337]
        
        print(f"{Colors.CYAN}[*] Monitoring for intrusions...{Colors.END}")
        print(f"{Colors.CYAN}[*] Suspicious ports: {suspicious_ports}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}\n")
        
        try:
            while True:
                for conn in psutil.net_connections():
                    if conn.status == 'ESTABLISHED' and conn.raddr:
                        if conn.raddr.port in suspicious_ports:
                            print(f"{Colors.RED}[!] ALERT: Suspicious connection on port {conn.raddr.port}{Colors.END}")
                            print(f"    From: {conn.raddr.ip}:{conn.raddr.port}")
                            print(f"    Process: {psutil.Process(conn.pid).name() if conn.pid else 'Unknown'}")
                            
                            # Log alert
                            with open(f"{self.log_dir}/ids_alerts.log", 'a') as f:
                                f.write(f"{datetime.now()}: ALERT from {conn.raddr.ip}:{conn.raddr.port}\n")
                time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] IDS stopped{Colors.END}")
    
    # ==================== MALWARE SCANNER ====================
    
    def malware_scanner(self):
        """Malware Scanner"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    MALWARE SCANNER                                   ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        target_dir = input(f"{self.prompt()}directory to scan > ") or self.home
        
        suspicious_patterns = [
            'reverse_shell', 'keylogger', 'ransomware', 'worm',
            'backdoor', 'trojan', 'exploit', 'payload',
            'socket.connect', 'subprocess.call', 'os.system'
        ]
        
        print(f"{Colors.CYAN}[*] Scanning {target_dir}...{Colors.END}\n")
        
        infected = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.py') or file.endswith('.sh') or file.endswith('.ps1'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', errors='ignore') as f:
                            content = f.read()
                            for pattern in suspicious_patterns:
                                if pattern in content.lower():
                                    print(f"{Colors.RED}[!] Suspicious: {filepath}{Colors.END}")
                                    infected.append(filepath)
                                    break
                    except:
                        pass
        
        print(f"\n{Colors.GREEN}[+] Found {len(infected)} suspicious files{Colors.END}")
        
        if infected:
            choice = input(f"{self.prompt()}Quarantine files? (y/n) > ")
            if choice.lower() == 'y':
                for f in infected:
                    filename = os.path.basename(f)
                    os.rename(f, f"{self.quarantine_dir}/{filename}")
                print(f"{Colors.GREEN}[+] Files quarantined to {self.quarantine_dir}{Colors.END}")
    
    # ==================== HONEYPOT MODULE ====================
    
    def honeypot_module(self):
        """Honeypot Deployment"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    HONEYPOT DEPLOYMENT                              ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} SSH Honeypot (port 22)")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} HTTP Honeypot (port 80)")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} FTP Honeypot (port 21)")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Custom Port")
        
        choice = input(self.prompt())
        
        def fake_service(port, service_name):
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', port))
                server.listen(5)
                print(f"{Colors.GREEN}[+] Honeypot running on port {port} ({service_name}){Colors.END}")
                print(f"{Colors.CYAN}[*] Waiting for connections...{Colors.END}\n")
                
                while True:
                    client, addr = server.accept()
                    print(f"{Colors.RED}[!] {service_name} connection from {addr[0]}:{addr[1]}{Colors.END}")
                    
                    # Send fake banner
                    if service_name == "SSH":
                        client.send(b"SSH-2.0-OpenSSH_8.2\r\n")
                    elif service_name == "HTTP":
                        client.send(b"HTTP/1.1 200 OK\r\n\r\n<h1>Welcome</h1>")
                    elif service_name == "FTP":
                        client.send(b"220 FTP Server ready\r\n")
                    
                    client.close()
                    
                    # Log attack
                    with open(f"{self.log_dir}/honeypot.log", 'a') as f:
                        f.write(f"{datetime.now()}: {service_name} attack from {addr[0]}:{addr[1]}\n")
            except:
                pass
        
        if choice == '1':
            threading.Thread(target=fake_service, args=(22, "SSH"), daemon=True).start()
        elif choice == '2':
            threading.Thread(target=fake_service, args=(80, "HTTP"), daemon=True).start()
        elif choice == '3':
            threading.Thread(target=fake_service, args=(21, "FTP"), daemon=True).start()
        elif choice == '4':
            port = int(input(f"{self.prompt()}Port > "))
            threading.Thread(target=fake_service, args=(port, f"Custom {port}"), daemon=True).start()
        
        input(f"{Colors.YELLOW}[*] Press Enter to stop honeypot...{Colors.END}")
    
    # ==================== BACKUP MODULE ====================
    
    def backup_module(self):
        """System Backup & Restore"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    SYSTEM BACKUP                                     ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Create Backup")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} List Backups")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Restore Backup")
        
        choice = input(self.prompt())
        
        if choice == '1':
            source = input(f"{self.prompt()}source directory > ")
            if not os.path.exists(source):
                print(f"{Colors.RED}[!] Source not found{Colors.END}")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.tar.gz"
            backup_path = f"{self.backup_dir}/{backup_name}"
            
            print(f"{Colors.CYAN}[*] Backing up {source}...{Colors.END}")
            os.system(f"tar -czf {backup_path} {source}")
            
            size = os.path.getsize(backup_path) // 1024
            print(f"{Colors.GREEN}[+] Backup saved: {backup_path}{Colors.END}")
            print(f"{Colors.GREEN}[+] Size: {size} KB{Colors.END}")
        
        elif choice == '2':
            backups = os.listdir(self.backup_dir)
            if backups:
                print(f"\n{Colors.CYAN}Available backups:{Colors.END}")
                for b in backups:
                    size = os.path.getsize(f"{self.backup_dir}/{b}") // 1024
                    print(f"  {b} - {size} KB")
            else:
                print(f"{Colors.YELLOW}[!] No backups found{Colors.END}")
        
        elif choice == '3':
            backups = os.listdir(self.backup_dir)
            if backups:
                print(f"\n{Colors.CYAN}Available backups:{Colors.END}")
                for i, b in enumerate(backups, 1):
                    print(f"  {i}. {b}")
                
                num = input(f"{self.prompt()}Select backup number > ")
                if num.isdigit() and 1 <= int(num) <= len(backups):
                    backup_file = f"{self.backup_dir}/{backups[int(num)-1]}"
                    target = input(f"{self.prompt()}restore to > ")
                    os.system(f"tar -xzf {backup_file} -C {target}")
                    print(f"{Colors.GREEN}[+] Restored to {target}{Colors.END}")
            else:
                print(f"{Colors.YELLOW}[!] No backups found{Colors.END}")
    
    # ==================== NETWORK MONITOR ====================
    
    def network_monitor(self):
        """Network Monitoring"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    NETWORK MONITOR                                    ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.CYAN}[*] Active Connections:{Colors.END}")
        
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                print(f"  {laddr} -> {raddr} ({conn.status})")
    
    # ==================== FILE ENCRYPTION ====================
    
    def encrypt_module(self):
        """File Encryption"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
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
                print(f"{Colors.GREEN}[+] Key: {filepath}.key{Colors.END}")
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
    
    # ==================== SECURITY AUDIT ====================
    
    def security_audit(self):
        """Security Audit"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    SECURITY AUDIT                                     ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        issues = []
        
        print(f"{Colors.CYAN}[*] Running security audit...{Colors.END}\n")
        
        # Check open ports
        print(f"{Colors.GREEN}[1] Checking open ports...{Colors.END}")
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                print(f"    Listening on {conn.laddr.ip}:{conn.laddr.port}")
        
        # Check running services
        print(f"\n{Colors.GREEN}[2] Checking running services...{Colors.END}")
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'ssh' in proc.info['name'].lower():
                print(f"    SSH running: {proc.info['name']}")
        
        # Check for suspicious files
        print(f"\n{Colors.GREEN}[3] Checking for suspicious files...{Colors.END}")
        suspicious_dirs = ['/tmp', self.home]
        patterns = ['reverse_shell', 'keylogger', 'backdoor']
        
        for dir_path in suspicious_dirs:
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.py'):
                            filepath = os.path.join(root, file)
                            try:
                                with open(filepath, 'r', errors='ignore') as f:
                                    content = f.read()
                                    for pattern in patterns:
                                        if pattern in content.lower():
                                            print(f"    {Colors.RED}Suspicious: {filepath}{Colors.END}")
                                            break
                            except:
                                pass
        
        print(f"\n{Colors.GREEN}[+] Audit complete. Found {len(issues)} issues.{Colors.END}")
    
    # ==================== LOG ANALYZER ====================
    
    def log_analyzer(self):
        """Log Analyzer"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    LOG ANALYZER                                       ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        logs = os.listdir(self.log_dir)
        if not logs:
            print(f"{Colors.YELLOW}[!] No logs found{Colors.END}")
            return
        
        print(f"{Colors.CYAN}Available logs:{Colors.END}")
        for i, log in enumerate(logs[:10], 1):
            size = os.path.getsize(f"{self.log_dir}/{log}") // 1024
            print(f"  {i}. {log} - {size} KB")
        
        choice = input(f"{self.prompt()}view log number > ")
        if choice.isdigit() and 1 <= int(choice) <= len(logs):
            logfile = f"{self.log_dir}/{logs[int(choice)-1]}"
            with open(logfile, 'r') as f:
                print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
                print(f.read())
                print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    # ==================== SYSTEM MONITOR ====================
    
    def system_monitor(self):
        """Real-time System Monitor"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    SYSTEM MONITOR                                     ║
║              "Watch the watchers"                                      ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        def monitor():
            try:
                while True:
                    os.system("clear")
                    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
                    print(f"{Colors.BOLD}SYSTEM MONITOR - {datetime.now()}{Colors.END}")
                    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
                    
                    # CPU
                    cpu_percent = psutil.cpu_percent(interval=1)
                    print(f"{Colors.GREEN}CPU Usage:{Colors.END} {cpu_percent}%")
                    
                    # Memory
                    mem = psutil.virtual_memory()
                    print(f"{Colors.GREEN}Memory:{Colors.END} {mem.percent}% ({mem.used//1024//1024}MB/{mem.total//1024//1024}MB)")
                    
                    # Disk
                    disk = psutil.disk_usage('/')
                    print(f"{Colors.GREEN}Disk:{Colors.END} {disk.percent}% ({disk.used//1024//1024}MB/{disk.total//1024//1024}MB)")
                    
                    # Network
                    net = psutil.net_io_counters()
                    print(f"{Colors.GREEN}Network:{Colors.END} Sent: {net.bytes_sent//1024}KB, Recv: {net.bytes_recv//1024}KB")
                    
                    # Active connections
                    connections = [c for c in psutil.net_connections() if c.status == 'ESTABLISHED']
                    print(f"\n{Colors.GREEN}Active Connections:{Colors.END} {len(connections)}")
                    
                    # Top processes
                    print(f"\n{Colors.GREEN}Top 5 Processes by CPU:{Colors.END}")
                    procs = sorted(psutil.process_iter(['name', 'cpu_percent']), 
                                  key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:5]
                    for p in procs:
                        print(f"  {p.info['name']}: {p.info['cpu_percent']}%")
                    
                    time.sleep(2)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Monitor stopped{Colors.END}")
        
        try:
            monitor()
        except KeyboardInterrupt:
            pass
    
    # ==================== ALERT CONFIGURATION ====================
    
    def alert_config(self):
        """Alert Configuration"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    ALERT CONFIGURATION                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Configure Email Alerts")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Configure Discord Webhook")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Test Alert")
        
        choice = input(self.prompt())
        
        if choice == '1':
            email = input(f"{self.prompt()}Email address > ")
            with open(f"{self.data_dir}/alert_email.txt", 'w') as f:
                f.write(email)
            print(f"{Colors.GREEN}[+] Alert email configured: {email}{Colors.END}")
        
        elif choice == '2':
            webhook = input(f"{self.prompt()}Discord Webhook URL > ")
            with open(f"{self.data_dir}/alert_discord.txt", 'w') as f:
                f.write(webhook)
            print(f"{Colors.GREEN}[+] Discord webhook configured{Colors.END}")
        
        elif choice == '3':
            print(f"{Colors.YELLOW}[!] Test alert sent{Colors.END}")
    
    # ==================== SYSTEM CLEANUP ====================
    
    def system_cleanup(self):
        """System Cleanup"""
        print(f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                    SYSTEM CLEANUP                                     ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Clean temp files")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} Clear logs")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Remove old backups")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} Full cleanup")
        
        choice = input(self.prompt())
        
        if choice == '1':
            os.system("rm -rf /tmp/* 2>/dev/null")
            os.system("rm -rf ~/.cache/* 2>/dev/null")
            print(f"{Colors.GREEN}[+] Temp files cleaned{Colors.END}")
        elif choice == '2':
            os.system("history -c")
            os.system("echo > ~/.bash_history")
            print(f"{Colors.GREEN}[+] Logs cleared{Colors.END}")
        elif choice == '3':
            os.system(f"rm -rf {self.backup_dir}/* 2>/dev/null")
            print(f"{Colors.GREEN}[+] Old backups removed{Colors.END}")
        elif choice == '4':
            os.system("rm -rf /tmp/* 2>/dev/null")
            os.system("history -c")
            os.system("echo > ~/.bash_history")
            print(f"{Colors.GREEN}[+] Full cleanup complete{Colors.END}")
    
    # ==================== HELP ====================
    
    def show_help(self):
        self.show_menu()
    
    # ==================== MAIN LOOP ====================
    
    def run(self):
        self.clear()
        
        while True:
            try:
                self.show_menu()
                cmd = input(self.prompt()).strip().lower()
                
                if cmd in ['firewall', 'fw']:
                    self.firewall_module()
                elif cmd in ['ids', 'i']:
                    self.ids_module()
                elif cmd in ['malware', 'm']:
                    self.malware_scanner()
                elif cmd in ['honeypot', 'hp']:
                    self.honeypot_module()
                elif cmd in ['backup', 'b']:
                    self.backup_module()
                elif cmd in ['network', 'n']:
                    self.network_monitor()
                elif cmd in ['encrypt', 'e']:
                    self.encrypt_module()
                elif cmd in ['audit', 'a']:
                    self.security_audit()
                elif cmd in ['log', 'l']:
                    self.log_analyzer()
                elif cmd in ['monitor', 'mon']:
                    self.system_monitor()
                elif cmd in ['alert', 'al']:
                    self.alert_config()
                elif cmd in ['clean', 'c']:
                    self.system_cleanup()
                elif cmd in ['clear', 'cls']:
                    self.clear()
                elif cmd in ['help', '?']:
                    self.show_help()
                elif cmd in ['exit', 'quit']:
                    print(f"{Colors.RED}[!] Shutting down...{Colors.END}")
                    sys.exit(0)
                elif cmd == '':
                    continue
                else:
                    print(f"{Colors.RED}[!] Unknown: {cmd}. Type 'help'{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Shutting down...{Colors.END}")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

if __name__ == "__main__":
    core = AwakenedCore()
    core.run()
