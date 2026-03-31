#!/usr/bin/env python3
# LAN SCANNER - Deteksi perangkat dalam jaringan lokal
# "Siapa aja yang connect ke WiFi lu?"

import subprocess
import re
import requests
import json
import os
from core.colors import Colors

class LANScanner:
    def __init__(self):
        self.name = "LAN Scanner"
        self.data_dir = os.path.expanduser("~/.duality/scans")
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_my_ip(self):
        """Dapatkan IP lokal sendiri"""
        try:
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            # Cari IP dalam jaringan lokal (192.168.x.x, 10.x.x.x, 172.x.x.x)
            match = re.search(r'inet (192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
        except:
            pass
        return "192.168.1.1"
    
    def get_network_range(self):
        """Dapatkan range jaringan lokal"""
        my_ip = self.get_my_ip()
        # Potong angka terakhir jadi .0/24
        network = '.'.join(my_ip.split('.')[:3]) + '.0/24'
        return network, my_ip
    
    def scan_arp(self):
        """Scan ARP untuk mendeteksi semua device"""
        network, my_ip = self.get_network_range()
        print(f"{Colors.CYAN}[*] Scanning network: {network}{Colors.END}")
        print(f"{Colors.CYAN}[*] Your IP: {my_ip}{Colors.END}\n")
        
        try:
            # Coba pake arp-scan
            result = subprocess.run(['arp-scan', '--localnet'], capture_output=True, text=True, timeout=30)
            devices = []
            
            # Parse output arp-scan
            for line in result.stdout.split('\n'):
                # Format arp-scan: IP\tMAC\tVendor
                parts = line.split('\t')
                if len(parts) >= 2 and re.match(r'\d+\.\d+\.\d+\.\d+', parts[0]):
                    ip = parts[0].strip()
                    mac = parts[1].strip() if len(parts) > 1 else "Unknown"
                    vendor = parts[2].strip() if len(parts) > 2 else "Unknown"
                    
                    if ip != my_ip:
                        devices.append({
                            'ip': ip,
                            'mac': mac,
                            'vendor': vendor,
                            'hostname': self.get_hostname(ip),
                            'os': self.detect_os(ip)
                        })
            
            return devices
            
        except FileNotFoundError:
            print(f"{Colors.RED}[!] arp-scan not installed!{Colors.END}")
            print(f"{Colors.YELLOW}[*] Install: pkg install arp-scan{Colors.END}")
            return []
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}[!] Scan timeout{Colors.END}")
            return []
    
    def get_hostname(self, ip):
        """Dapatkan hostname dari IP"""
        try:
            result = subprocess.run(['nslookup', ip], capture_output=True, text=True, timeout=5)
            # Cari nama host
            match = re.search(r'name = (.+)\.', result.stdout)
            if match:
                return match.group(1)
        except:
            pass
        return "Unknown"
    
    def detect_os(self, ip):
        """Deteksi OS pake nmap (simple)"""
        try:
            # Cek TTL dari ping
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=5)
            # Cari TTL
            ttl_match = re.search(r'ttl=(\d+)', result.stdout.lower())
            if ttl_match:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    return "Linux/Unix"
                elif ttl <= 128:
                    return "Windows"
                elif ttl <= 255:
                    return "Cisco/Network"
        except:
            pass
        return "Unknown"
    
    def get_device_type(self, vendor, hostname, os):
        """Tentukan tipe device berdasarkan data"""
        vendor_lower = vendor.lower()
        hostname_lower = hostname.lower()
        
        if 'android' in hostname_lower or 'samsung' in vendor_lower or 'xiaomi' in vendor_lower:
            return "📱 Android Phone"
        elif 'iphone' in hostname_lower or 'ipad' in hostname_lower or 'apple' in vendor_lower:
            return "📱 Apple Device"
        elif 'windows' in os.lower() or 'win' in hostname_lower:
            return "💻 Windows PC"
        elif 'linux' in os.lower() or 'ubuntu' in hostname_lower:
            return "🐧 Linux PC"
        elif 'raspberry' in hostname_lower:
            return "🍓 Raspberry Pi"
        elif 'router' in hostname_lower or 'gateway' in hostname_lower:
            return "🌐 Router"
        elif 'tv' in hostname_lower or 'samsung' in vendor_lower:
            return "📺 Smart TV"
        else:
            return "❓ Unknown Device"
    
    def get_icon(self, device_type):
        """Dapatkan icon untuk tipe device"""
        icons = {
            "📱 Android Phone": "🤖",
            "📱 Apple Device": "🍎",
            "💻 Windows PC": "🪟",
            "🐧 Linux PC": "🐧",
            "🍓 Raspberry Pi": "🥧",
            "🌐 Router": "📡",
            "📺 Smart TV": "📺",
            "❓ Unknown Device": "❓"
        }
        return icons.get(device_type, "💻")
    
    def scan_ports(self, ip, ports="22,80,443,8080,5555"):
        """Scan port terbuka pada device"""
        open_ports = []
        port_list = [int(p) for p in ports.split(',')]
        
        print(f"{Colors.DIM}[*] Scanning ports on {ip}...{Colors.END}")
        
        for port in port_list:
            try:
                result = subprocess.run(['nc', '-zv', '-w', '1', ip, str(port)], 
                                       capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    open_ports.append(port)
            except:
                pass
        
        return open_ports
    
    def get_port_service(self, port):
        """Dapatkan nama service dari port"""
        services = {
            22: "SSH",
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP-Alt",
            5555: "ADB (Android Debug)",
            3306: "MySQL",
            5432: "PostgreSQL",
            5900: "VNC",
            3389: "RDP"
        }
        return services.get(port, "Unknown")
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       🌐 LAN SCANNER - Network Discovery{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Quick Scan (ARP + Ping)")
        print(f"{Colors.GREEN}[2]{Colors.END} Full Scan (ARP + OS Detection)")
        print(f"{Colors.GREEN}[3]{Colors.END} Port Scan on Device")
        print(f"{Colors.GREEN}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.quick_scan()
        elif choice == '2':
            self.full_scan()
        elif choice == '3':
            self.port_scan_menu()
    
    def quick_scan(self):
        """Quick scan - cuma ARP + ping"""
        print(f"\n{Colors.CYAN}[*] Quick Scan Started{Colors.END}\n")
        
        devices = self.scan_arp()
        
        if not devices:
            print(f"{Colors.RED}[!] No devices found or scan failed{Colors.END}")
            return
        
        print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}📡 ACTIVE DEVICES{Colors.END}")
        print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
        
        for i, device in enumerate(devices, 1):
            device_type = self.get_device_type(device['vendor'], device['hostname'], device['os'])
            icon = self.get_icon(device_type)
            
            print(f"\n{Colors.CYAN}[{i}]{Colors.END} {icon} {device['ip']}")
            print(f"   📍 MAC: {device['mac']}")
            print(f"   🏷️  Vendor: {device['vendor']}")
            print(f"   💻 Hostname: {device['hostname']}")
            print(f"   🔍 Type: {device_type}")
        
        # Save result
        self.save_results(devices)
    
    def full_scan(self):
        """Full scan dengan OS detection"""
        print(f"\n{Colors.CYAN}[*] Full Scan Started (may take a while){Colors.END}\n")
        
        devices = self.scan_arp()
        
        if not devices:
            print(f"{Colors.RED}[!] No devices found{Colors.END}")
            return
        
        print(f"{Colors.CYAN}[*] Detecting OS for each device...{Colors.END}\n")
        
        for device in devices:
            # OS detection lebih akurat pake nmap (opsional)
            try:
                result = subprocess.run(['nmap', '-O', '--osscan-guess', device['ip']], 
                                       capture_output=True, text=True, timeout=30)
                # Parse OS dari output nmap
                os_match = re.search(r'OS details: (.+)', result.stdout)
                if os_match:
                    device['os'] = os_match.group(1)[:50]
            except:
                pass
        
        print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}📡 DEVICE DETAILS{Colors.END}")
        print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
        
        for i, device in enumerate(devices, 1):
            device_type = self.get_device_type(device['vendor'], device['hostname'], device['os'])
            icon = self.get_icon(device_type)
            
            print(f"\n{Colors.CYAN}[{i}]{Colors.END} {icon} {device['ip']}")
            print(f"   📍 MAC: {device['mac']}")
            print(f"   🏷️  Vendor: {device['vendor']}")
            print(f"   💻 Hostname: {device['hostname']}")
            print(f"   🔍 Type: {device_type}")
            print(f"   ⚙️  OS: {device['os']}")
        
        self.save_results(devices)
    
    def port_scan_menu(self):
        """Menu scan port pada device tertentu"""
        print(f"\n{Colors.CYAN}[*] Port Scan on Device{Colors.END}")
        
        # Scan dulu buat dapetin device list
        devices = self.scan_arp()
        
        if not devices:
            print(f"{Colors.RED}[!] No devices found{Colors.END}")
            return
        
        print(f"\n{Colors.GREEN}Select device:{Colors.END}")
        for i, device in enumerate(devices, 1):
            print(f"  {Colors.CYAN}[{i}]{Colors.END} {device['ip']} ({device['vendor']})")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice.isdigit() and 1 <= int(choice) <= len(devices):
            device = devices[int(choice)-1]
            target_ip = device['ip']
            
            print(f"\n{Colors.CYAN}[*] Scanning ports on {target_ip}{Colors.END}")
            print(f"{Colors.YELLOW}[!] This may take a moment...{Colors.END}\n")
            
            ports = input(f"{Colors.GREEN}Ports to scan (default: 22,80,443,8080,5555) > {Colors.END}")
            if not ports:
                ports = "22,80,443,8080,5555"
            
            open_ports = self.scan_ports(target_ip, ports)
            
            if open_ports:
                print(f"\n{Colors.GREEN}{'═'*55}{Colors.END}")
                print(f"{Colors.BOLD}🔓 OPEN PORTS ON {target_ip}{Colors.END}")
                print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
                for port in open_ports:
                    service = self.get_port_service(port)
                    print(f"  {Colors.GREEN}[✓]{Colors.END} Port {port}: {service}")
            else:
                print(f"\n{Colors.YELLOW}[!] No open ports found{Colors.END}")
    
    def save_results(self, devices):
        """Simpan hasil scan ke file"""
        import json
        from datetime import datetime
        
        filename = f"{self.data_dir}/lan_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(devices, f, indent=2)
        
        print(f"\n{Colors.GREEN}[+] Results saved to: {filename}{Colors.END}")

if __name__ == "__main__":
    scanner = LANScanner()
    scanner.run()
