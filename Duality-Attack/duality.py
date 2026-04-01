#!/usr/bin/env python3
# DUALITY ATTACK v3.0 - Complete Edition (31 Modules)
# "The darkness that consumes the light"
import sys
import os
from core.colors import Colors
from core.utils import clear_screen
from config.settings import VERSION

# OSINT (9)
from modules.osint.phone import PhoneOSINT
from modules.osint.ip import IPTracker
from modules.osint.username import UsernameOSINT
from modules.osint.subdomain import SubdomainScanner
from modules.osint.port import PortScanner
from modules.osint.dork import DorkGenerator
from modules.osint.email import EmailOSINT
from modules.osint.whois import WHOISLookup
from modules.osint.dns import DNSLookup

# Attack (13)
from modules.attack.payload import PayloadGenerator
from modules.attack.ddos import DDoSModule
from modules.attack.stealth import StealthCleaner
from modules.attack.anon import AnonymityModule
from modules.attack.c2 import C2Server
from modules.attack.scanner.lan_scanner import LANScanner
from modules.attack.enumeration.subdomain_enum import SubdomainEnum
from modules.attack.enumeration.email_scraper import EmailScraper
from modules.attack.enumeration.link_extractor import LinkExtractor
from modules.attack.enumeration.dir_brute import DirBrute
from modules.attack.enumeration.port_scanner_advanced import PortScannerAdvanced
from modules.attack.advanced_attack.phishing_gen import PhishingGenerator
from modules.attack.advanced_attack.wifi_cracker import WiFiCracker
from modules.attack.advanced_attack.cam_hack import CameraHack
from modules.attack.advanced_attack.pentest_report import PentestReport
from modules.attack.advanced_attack.ddos_panel import DDoSPanel
from modules.attack.advanced_attack.exploit_db import ExploitDB

# Utility (5)
from modules.utility.crypt import FileCrypt
from modules.utility.hash import HashGenerator
from modules.utility.encode import EncodeDecode
from modules.utility.passgen import PasswordGenerator
from modules.utility.malware import EducationalMalware
from modules.attack.tracking.phone_tracker import PhoneTracker
from modules.attack.spam.spammer import Spammer
from modules.utility.rot13 import ROT13Tool
from modules.utility.finder import FindWrapper
from modules.attack.ai_scanner.ai_assistant import AIAssistant
from modules.attack.ai_scanner.vuln_scanner import VulnScanner
from modules.utility.qr_gen import QRGenerator
from modules.utility.speedtest import SpeedTest

# Botnet (1)
from modules.botnet.server import BotnetServer

# Advanced (11)
from modules.advanced.ai import AIIntegration
from modules.advanced.exploit import AutoExploiter
from modules.advanced.persistence import PersistenceModule
from modules.advanced.transfer import FileTransfer
from modules.advanced.screenshot import ScreenshotModule
from modules.advanced.keylogger import KeyloggerModule
from modules.advanced.password_stealer import PasswordStealer
from modules.advanced.crypto_miner import CryptoMiner
from modules.advanced.auto_updater import AutoUpdater
from modules.advanced.darkweb_c2 import DarkWebC2
from modules.advanced.webcam import WebcamCapture
from modules.attack.tracking.phone_tracker import PhoneTracker
from modules.attack.spam.spammer import Spammer
from modules.attack.c2_gui.c2_gui import C2GUI
from modules.attack.darkweb.darkweb_integration import DarkWebIntegration
from modules.attack.social.social_scraper import SocialMediaScraper
from modules.advanced.forensics.memory_forensics import MemoryForensics
from modules.advanced.ai_agents.orchestrator import AIOrchestrator

class DualityAttack:
    def __init__(self):
        self.version = VERSION
        self.modules = {
            # OSINT (9)
            'phone': PhoneOSINT(),
            'ip': IPTracker(),
            'username': UsernameOSINT(),
            'subdomain': SubdomainScanner(),
            'port': PortScanner(),
            'dork': DorkGenerator(),
            'email': EmailOSINT(),
            'whois': WHOISLookup(),
            'dns': DNSLookup(),
            # Attack (13)
            'payload': PayloadGenerator(),
            'ddos': DDoSModule(),
            'stealth': StealthCleaner(),
            'anon': AnonymityModule(),
            'c2': C2Server(),
            'track': PhoneTracker(),
            'spam': Spammer(),
            'lanscan': LANScanner(),
            'subenum': SubdomainEnum(),
            'emailscrape': EmailScraper(),
            'linkextract': LinkExtractor(),
            'dirbrute': DirBrute(),
            'portadv': PortScannerAdvanced(),
            'phish': PhishingGenerator(),
            'wificrack': WiFiCracker(),
            'camhack': CameraHack(),
            'pentest': PentestReport(),
            'ddospanel': DDoSPanel(),
            'exploitdb': ExploitDB(),
            # Utility (5)
            'crypt': FileCrypt(),
            'hash': HashGenerator(),
            'encode': EncodeDecode(),
            'passgen': PasswordGenerator(),
            'malware': EducationalMalware(),
            'rot13': ROT13Tool(),
            'find': FindWrapper(),
            'aiassist': AIAssistant(),
            'vulnscan': VulnScanner(),
            'qr': QRGenerator(),
            'speedtest': SpeedTest(),
            # Botnet (1)
            'botnet': BotnetServer(),
            # Advanced (11)
            'ai': AIIntegration(),
            'exploit': AutoExploiter(),
            'persist': PersistenceModule(),
            'transfer': FileTransfer(),
            'screenshot': ScreenshotModule(),
            'keylog': KeyloggerModule(),
            'steal': PasswordStealer(),
            'miner': CryptoMiner(),
            'update': AutoUpdater(),
            'darkweb': DarkWebC2(),
            'webcam': WebcamCapture(),
            'c2gui': C2GUI(),
            'darkweb': DarkWebIntegration(),
            'social': SocialMediaScraper(),
            'memforensics': MemoryForensics(),
            'aiorchestrator': AIOrchestrator(),
            }
        
    def banner(self):
        """Tampilkan logo dan banner"""
        clear_screen()

    # Coba tampilkan logo skull (txt, BUKAN png)
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'skull_logo.txt')
        if os.path.exists(logo_path):
            with open(logo_path, 'r') as f:
                print(f.read())
        else:
        # Fallback jika logo tidak ada
            print(f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                    DUALITY ATTACK v{self.version}                     ║
║              "The darkness that consumes the light"            ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
        """)
        print(f"{Colors.RED}{Colors.BOLD}                              DUALITY ATTACK v{self.version}{Colors.END}")
        print(f"{Colors.DIM}                           \"The darkness that consumes the light\"{Colors.END}")
        print(f"{Colors.RED}{'═'*71}{Colors.END}")
        
    def show_help(self):
        help_text = f"""
{Colors.RED}{'═'*79}{Colors.END}
{Colors.BOLD}{Colors.WHITE}                         DUALITY ATTACK - COMPLETE EDITION{Colors.END}
{Colors.RED}{'═'*79}{Colors.END}

{Colors.RED}{Colors.BOLD}📱 OSINT MODULES ({Colors.WHITE}9 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}phone{Colors.DIM}      - Phone number OSINT with carrier detection
{Colors.WHITE}  {Colors.WHITE}ip{Colors.DIM}         - IP address geolocation tracker
{Colors.WHITE}  {Colors.WHITE}username{Colors.DIM}   - Check username across social media
{Colors.WHITE}  {Colors.WHITE}subdomain{Colors.DIM}  - Subdomain discovery scanner
{Colors.WHITE}  {Colors.WHITE}port{Colors.DIM}       - TCP port scanner (1-1000)
{Colors.WHITE}  {Colors.WHITE}dork{Colors.DIM}       - Google dork generator
{Colors.WHITE}  {Colors.WHITE}email{Colors.DIM}      - Email OSINT / breach check
{Colors.WHITE}  {Colors.WHITE}whois{Colors.DIM}      - WHOIS domain lookup
{Colors.WHITE}  {Colors.WHITE}dns{Colors.DIM}        - DNS records lookup (A, MX, NS, TXT)

{Colors.RED}{Colors.BOLD}⚔️ ATTACK MODULES ({Colors.WHITE}8 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}payload{Colors.DIM}    - Generate reverse shell (Python/Bash/PHP)
{Colors.WHITE}  {Colors.WHITE}ddos{Colors.DIM}       - DDoS attack simulation
{Colors.WHITE}  {Colors.WHITE}stealth{Colors.DIM}    - Clean traces, wipe logs
{Colors.WHITE}  {Colors.WHITE}anon{Colors.DIM}       - Anonymity (Tor network)
{Colors.WHITE}  {Colors.WHITE}c2{Colors.DIM}         - C2 / Listener server (HTTP/Netcat)
{Colors.WHITE}  {Colors.WHITE}track{Colors.DIM}      - Phone number tracker
{Colors.WHITE}  {Colors.WHITE}spam{Colors.DIM}       - Email/SMS spammer
{Colors.WHITE}  {Colors.WHITE}lanscan{Colors.DIM}     - LAN network scanner (detect devices)
{Colors.WHITE}  {Colors.WHITE}subenum{Colors.DIM}     - Subdomain enumeration
{Colors.WHITE}  {Colors.WHITE}emailscrape{Colors.DIM} - Email scraper from website
{Colors.WHITE}  {Colors.WHITE}linkextract{Colors.DIM} - Extract all links
{Colors.WHITE}  {Colors.WHITE}dirbrute{Colors.DIM}    - Directory brute force
{Colors.WHITE}  {Colors.WHITE}portadv{Colors.DIM}     - Advanced port scanner

{Colors.RED}{Colors.BOLD}🔥 ADVANCED ATTACK ({Colors.WHITE}6 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}phish{Colors.DIM}      - Phishing page generator
{Colors.WHITE}  {Colors.WHITE}wificrack{Colors.DIM}  - WiFi password cracker
{Colors.WHITE}  {Colors.WHITE}camhack{Colors.DIM}    - Live camera hack
{Colors.WHITE}  {Colors.WHITE}pentest{Colors.DIM}    - Auto pentest report
{Colors.WHITE}  {Colors.WHITE}ddospanel{Colors.DIM}  - DDoS web panel
{Colors.WHITE}  {Colors.WHITE}exploitdb{Colors.DIM}  - Auto exploit database
{Colors.WHITE}  {Colors.WHITE}vulnscan{Colors.DIM}   - Auto vulnerability scanner

{Colors.RED}🛠️ UTILITY MODULES ({Colors.WHITE}7 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}crypt{Colors.DIM}      - AES file encryption/decryption
{Colors.WHITE}  {Colors.WHITE}hash{Colors.DIM}       - Hash generator (MD5/SHA1/SHA256)
{Colors.WHITE}  {Colors.WHITE}encode{Colors.DIM}     - Base64/URL encoder decoder
{Colors.WHITE}  {Colors.WHITE}passgen{Colors.DIM}    - Random password generator
{Colors.WHITE}  {Colors.WHITE}malware{Colors.DIM}    - Educational malware generator
{Colors.WHITE}  {Colors.WHITE}rot13{Colors.DIM}      - ROT13 cipher encoder/decoder
{Colors.WHITE}  {Colors.WHITE}find{Colors.DIM}       - Find command wrapper
{Colors.WHITE}  {Colors.WHITE}aiassist{Colors.DIM}   - AI Assistant chatbot
{Colors.WHITE}  {Colors.WHITE}qr{Colors.DIM}         - QR Code generator
{Colors.WHITE}  {Colors.WHITE}speedtest{Colors.DIM}  - Network speed test

{Colors.RED}{Colors.BOLD}🤖 BOTNET MODULES ({Colors.WHITE}1 module{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}botnet{Colors.DIM}     - Botnet C2 server (HTTP API)

{Colors.RED}{Colors.BOLD}🚀 ADVANCED MODULES ({Colors.WHITE}11 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.WHITE}ai{Colors.DIM}         - AI payload generator & vulnerability analysis
{Colors.WHITE}  {Colors.WHITE}exploit{Colors.DIM}    - Auto exploiter (SQLi/XSS/LFI scanner)
{Colors.WHITE}  {Colors.WHITE}persist{Colors.DIM}    - Persistence module (cron/systemd)
{Colors.WHITE}  {Colors.WHITE}transfer{Colors.DIM}   - File upload/download
{Colors.WHITE}  {Colors.WHITE}screenshot{Colors.DIM} - Screenshot capture (termux-api)
{Colors.WHITE}  {Colors.WHITE}keylog{Colors.DIM}     - Keylogger (record keystrokes)
{Colors.WHITE}  {Colors.WHITE}steal{Colors.DIM}      - Password stealer (Chrome/SSH)
{Colors.WHITE}  {Colors.WHITE}miner{Colors.DIM}      - Crypto miner (XMRig simulation)
{Colors.WHITE}  {Colors.WHITE}update{Colors.DIM}     - Auto updater (git pull)
{Colors.WHITE}  {Colors.WHITE}darkweb{Colors.DIM}    - Dark web C2 (Tor hidden service)
{Colors.WHITE}  {Colors.WHITE}webcam{Colors.DIM}     - Webcam capture (termux-api)
{Colors.WHITE}  {Colors.WHITE}c2gui{Colors.DIM}     - C2 Server with GUI dashboard
{Colors.WHITE}  {Colors.WHITE}darkweb{Colors.DIM}   - Dark web integration (Tor)
{Colors.WHITE}  {Colors.WHITE}social{Colors.DIM}    - Social media scraper
{Colors.WHITE}  {Colors.WHITE}memforensics{Colors.DIM} - Memory forensics (capture & analyze)
{Colors.WHITE}  {Colors.WHITE}aiorchestrator{Colors.DIM} - AI multi-agent orchestrator

{Colors.RED}{Colors.BOLD}⚙️ SYSTEM COMMANDS{Colors.END}
{Colors.WHITE}  {Colors.WHITE}help{Colors.DIM}       - Show this help menu
{Colors.WHITE}  {Colors.WHITE}clear{Colors.DIM}      - Clear screen
{Colors.WHITE}  {Colors.WHITE}exit{Colors.DIM}       - Exit DUALITY

{Colors.RED}{'═'*79}{Colors.END}
{Colors.DIM}[*] Type any module name to run it | Example: phone, ip, username, help{Colors.END}
{Colors.RED}{'═'*79}{Colors.END}
        """
        print(help_text)
    
    def run(self):
        self.banner()
        
        while True:
            try:
                cmd = input(f"\n{Colors.WHITE}┌──({Colors.RED}duality{Colors.RED}@{Colors.RED}attack{Colors.WHITE})-{Colors.DIM}[{os.getcwd().replace(os.path.expanduser('~'), '~')}]{Colors.WHITE}\n└─{Colors.RED}$ {Colors.END}").strip().lower()
                
                if cmd == 'exit':
                    print(f"\n{Colors.RED}[!] Exiting DUALITY...{Colors.END}")
                    sys.exit(0)
                elif cmd == 'clear':
                    self.banner()
                elif cmd == 'help':
                    self.show_help()
                elif cmd in self.modules:
                    self.modules[cmd].run()
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")
                    self.banner()
                elif cmd:
                    from core.utils import print_error
                    print_error(f"Unknown command: '{cmd}'", show_tip=True)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Interrupted. Exiting...{Colors.END}")
                sys.exit(0)
            except Exception as e:
                from core.utils import print_error
                print_error(str(e))
if __name__ == "__main__":
    app = DualityAttack()
    app.run()
