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
            }
        
    def banner(self):
        clear_screen()
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║   ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗████████╗██╗   ██╗                            ║
║   ██╔══██╗██║   ██║██╔══██╗██║     ██║╚══██╔══╝╚██╗ ██╔╝                            ║
║   ██║  ██║██║   ██║███████║██║     ██║   ██║    ╚████╔╝                             ║
║   ██║  ██║██║   ██║██╔══██║██║     ██║   ██║     ╚██╔╝                              ║
║   ██████╔╝╚██████╔╝██║  ██║███████╗██║   ██║      ██║                               ║
║   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝                               ║
║                                                                                       ║
║   █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗                                  ║
║   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝                                  ║
║   ███████║   ██║      ██║   ███████║██║     █████╔╝                                   ║
║   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗                                   ║
║   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗                                  ║
║   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                                  ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.CYAN}{Colors.BOLD}                         DUALITY ATTACK v{self.version}{Colors.END}
{Colors.DIM}                              "The darkness that consumes the light"{Colors.END}
{Colors.RED}{'═'*79}{Colors.END}
        """
        print(banner)
    
    def show_help(self):
        help_text = f"""
{Colors.RED}{'═'*79}{Colors.END}
{Colors.BOLD}{Colors.WHITE}                         DUALITY ATTACK - COMPLETE EDITION{Colors.END}
{Colors.RED}{'═'*79}{Colors.END}

{Colors.CYAN}{Colors.BOLD}📱 OSINT MODULES ({Colors.GREEN}9 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}phone{Colors.WHITE}      - Phone number OSINT with carrier detection
{Colors.WHITE}  {Colors.GREEN}ip{Colors.WHITE}         - IP address geolocation tracker
{Colors.WHITE}  {Colors.GREEN}username{Colors.WHITE}   - Check username across social media
{Colors.WHITE}  {Colors.GREEN}subdomain{Colors.WHITE}  - Subdomain discovery scanner
{Colors.WHITE}  {Colors.GREEN}port{Colors.WHITE}       - TCP port scanner (1-1000)
{Colors.WHITE}  {Colors.GREEN}dork{Colors.WHITE}       - Google dork generator
{Colors.WHITE}  {Colors.GREEN}email{Colors.WHITE}      - Email OSINT / breach check
{Colors.WHITE}  {Colors.GREEN}whois{Colors.WHITE}      - WHOIS domain lookup
{Colors.WHITE}  {Colors.GREEN}dns{Colors.WHITE}        - DNS records lookup (A, MX, NS, TXT)

{Colors.CYAN}{Colors.BOLD}⚔️ ATTACK MODULES ({Colors.GREEN}8 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}payload{Colors.WHITE}    - Generate reverse shell (Python/Bash/PHP)
{Colors.WHITE}  {Colors.GREEN}ddos{Colors.WHITE}       - DDoS attack simulation
{Colors.WHITE}  {Colors.GREEN}stealth{Colors.WHITE}    - Clean traces, wipe logs
{Colors.WHITE}  {Colors.GREEN}anon{Colors.WHITE}       - Anonymity (Tor network)
{Colors.WHITE}  {Colors.GREEN}c2{Colors.WHITE}         - C2 / Listener server (HTTP/Netcat)
{Colors.WHITE}  {Colors.GREEN}track{Colors.WHITE}      - Phone number tracker
{Colors.WHITE}  {Colors.GREEN}spam{Colors.WHITE}       - Email/SMS spammer
{Colors.WHITE}  {Colors.GREEN}lanscan{Colors.WHITE}     - LAN network scanner (detect devices)
{Colors.WHITE}  {Colors.GREEN}subenum{Colors.WHITE}     - Subdomain enumeration
{Colors.WHITE}  {Colors.GREEN}emailscrape{Colors.WHITE} - Email scraper from website
{Colors.WHITE}  {Colors.GREEN}linkextract{Colors.WHITE} - Extract all links
{Colors.WHITE}  {Colors.GREEN}dirbrute{Colors.WHITE}    - Directory brute force
{Colors.WHITE}  {Colors.GREEN}portadv{Colors.WHITE}     - Advanced port scanner

{Colors.CYAN}{Colors.BOLD}🔥 ADVANCED ATTACK ({Colors.GREEN}6 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}phish{Colors.WHITE}      - Phishing page generator
{Colors.WHITE}  {Colors.GREEN}wificrack{Colors.WHITE}  - WiFi password cracker
{Colors.WHITE}  {Colors.GREEN}camhack{Colors.WHITE}    - Live camera hack
{Colors.WHITE}  {Colors.GREEN}pentest{Colors.WHITE}    - Auto pentest report
{Colors.WHITE}  {Colors.GREEN}ddospanel{Colors.WHITE}  - DDoS web panel
{Colors.WHITE}  {Colors.GREEN}exploitdb{Colors.WHITE}  - Auto exploit database

{Colors.CYAN}🛠️ UTILITY MODULES ({Colors.GREEN}7 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}crypt{Colors.WHITE}      - AES file encryption/decryption
{Colors.WHITE}  {Colors.GREEN}hash{Colors.WHITE}       - Hash generator (MD5/SHA1/SHA256)
{Colors.WHITE}  {Colors.GREEN}encode{Colors.WHITE}     - Base64/URL encoder decoder
{Colors.WHITE}  {Colors.GREEN}passgen{Colors.WHITE}    - Random password generator
{Colors.WHITE}  {Colors.GREEN}malware{Colors.WHITE}    - Educational malware generator
{Colors.WHITE}  {Colors.GREEN}rot13{Colors.WHITE}      - ROT13 cipher encoder/decoder
{Colors.WHITE}  {Colors.GREEN}find{Colors.WHITE}       - Find command wrapper

{Colors.CYAN}{Colors.BOLD}🤖 BOTNET MODULES ({Colors.GREEN}1 module{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}botnet{Colors.WHITE}     - Botnet C2 server (HTTP API)

{Colors.CYAN}{Colors.BOLD}🚀 ADVANCED MODULES ({Colors.GREEN}11 modules{Colors.CYAN}){Colors.END}
{Colors.WHITE}  {Colors.GREEN}ai{Colors.WHITE}         - AI payload generator & vulnerability analysis
{Colors.WHITE}  {Colors.GREEN}exploit{Colors.WHITE}    - Auto exploiter (SQLi/XSS/LFI scanner)
{Colors.WHITE}  {Colors.GREEN}persist{Colors.WHITE}    - Persistence module (cron/systemd)
{Colors.WHITE}  {Colors.GREEN}transfer{Colors.WHITE}   - File upload/download
{Colors.WHITE}  {Colors.GREEN}screenshot{Colors.WHITE} - Screenshot capture (termux-api)
{Colors.WHITE}  {Colors.GREEN}keylog{Colors.WHITE}     - Keylogger (record keystrokes)
{Colors.WHITE}  {Colors.GREEN}steal{Colors.WHITE}      - Password stealer (Chrome/SSH)
{Colors.WHITE}  {Colors.GREEN}miner{Colors.WHITE}      - Crypto miner (XMRig simulation)
{Colors.WHITE}  {Colors.GREEN}update{Colors.WHITE}     - Auto updater (git pull)
{Colors.WHITE}  {Colors.GREEN}darkweb{Colors.WHITE}    - Dark web C2 (Tor hidden service)
{Colors.WHITE}  {Colors.GREEN}webcam{Colors.WHITE}     - Webcam capture (termux-api)

{Colors.CYAN}{Colors.BOLD}⚙️ SYSTEM COMMANDS{Colors.END}
{Colors.WHITE}  {Colors.GREEN}help{Colors.WHITE}       - Show this help menu
{Colors.WHITE}  {Colors.GREEN}clear{Colors.WHITE}      - Clear screen
{Colors.WHITE}  {Colors.GREEN}exit{Colors.WHITE}       - Exit DUALITY

{Colors.RED}{'═'*79}{Colors.END}
{Colors.DIM}[*] Type any module name to run it | Example: phone, ip, username, help{Colors.END}
{Colors.RED}{'═'*79}{Colors.END}
        """
        print(help_text)
    
    def run(self):
        self.banner()
        
        while True:
            try:
                cmd = input(f"\n{Colors.RED}┌──({Colors.RED}duality{Colors.RED}@{Colors.RED}attack{Colors.RED})-{Colors.RED}[{os.getcwd().replace(os.path.expanduser('~'), '~')}]{Colors.RED}\n└─{Colors.WHITE}$ {Colors.END}").strip().lower()
                
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
                    print(f"{Colors.RED}[!] Unknown command: {cmd}{Colors.END}")
                    print(f"{Colors.DIM}[*] Type 'help' for available commands{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Interrupted. Exiting...{Colors.END}")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

if __name__ == "__main__":
    app = DualityAttack()
    app.run()
