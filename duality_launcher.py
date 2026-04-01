#!/usr/bin/env python3
# DUALITY LAUNCHER - Cek IP dulu, baru Matrix Rain

import os
import sys
import time
import random
import subprocess
import json
from core.utils import loading_animation
# Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def clear_screen():
    os.system('clear')

def matrix_rain_hijau(duration=5, fall_speed=1.5):
    """
    Animasi Matrix rain - warna hijau klasik
    """
    # Ukuran terminal
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    
    # Karakter beragam
    chars = "ktoncTTXCL5@#CNQrmsbUVrpf aM(w eouk%GehF iJijl.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    
    # Warna hijau khas Matrix
    GREEN_BRIGHT = '\033[92m'    # Hijau terang (kepala)
    GREEN_MEDIUM = '\033[32m'    # Hijau sedang
    GREEN_DARK = '\033[38;5;22m' # Hijau gelap (ekor)
    WHITE = '\033[97m'           # Putih (aksen)
    BLACK = '\033[30m'           # Hitam (background)
    
    # Background hitam
    print('\033[40m', end='')
    
    # Posisi setiap kolom
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.2, 0.5) * fall_speed,
            'length': random.randint(5, 15),
        })
    
    end_time = time.time() + duration
    
    try:
        while time.time() < end_time:
            # Buat frame
            frame = [[' ' for _ in range(columns)] for _ in range(rows)]
            
            # Update setiap kolom
            for x in range(columns):
                data = columns_data[x]
                data['y'] += data['speed']
                
                if data['y'] > rows + data['length']:
                    data['y'] = -data['length']
                    data['speed'] = random.uniform(0.2, 0.5) * fall_speed
                    data['length'] = random.randint(5, 15)
                
                # Gambar trail dengan warna hijau
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        char = random.choice(chars)
                        if i == 0:
                            # Kepala: Hijau terang
                            frame[y][x] = f"{GREEN_BRIGHT}{char}\033[0m\033[40m"
                        elif i == 1:
                            # Kedua: Putih (opsional, biar keliatan keren)
                            frame[y][x] = f"{WHITE}{char}\033[0m\033[40m"
                        elif i == 2:
                            # Ketiga: Hijau sedang
                            frame[y][x] = f"{GREEN_MEDIUM}{char}\033[0m\033[40m"
                        else:
                            # Ekor: Hijau gelap atau hitam
                            if random.choice([True, False]):
                                frame[y][x] = f"{GREEN_DARK}{char}\033[0m\033[40m"
                            else:
                                frame[y][x] = f"{BLACK}{char}\033[0m\033[40m"
            
            # Render frame
            output = []
            for y in range(rows):
                output.append(''.join(frame[y]))
            
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(output))
            sys.stdout.flush()
            
            time.sleep(0.03)
    
    except KeyboardInterrupt:
        pass
    
    print("\033[0m" * rows)
    os.system('clear')

def check_ip():
    """Cek IP publik dan lokasi"""
    print(f"\n{Colors.CYAN}{'═'*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}🔍 VERIFIKASI SISTEM{Colors.END}")
    print(f"{Colors.CYAN}{'═'*60}{Colors.END}\n")
    
    try:
        import requests
        
        # Cek IP
        print(f"{Colors.YELLOW}[*] Mengecek IP publik...{Colors.END}")
        ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"{Colors.GREEN}[✓] IP Publik: {Colors.WHITE}{ip}{Colors.END}")
        
        # Cek lokasi
        print(f"{Colors.YELLOW}[*] Mengecek lokasi...{Colors.END}")
        geo = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        
        if geo.get('status') == 'success':
            print(f"{Colors.GREEN}[✓] Lokasi: {Colors.WHITE}{geo.get('city')}, {geo.get('country')}{Colors.END}")
            print(f"{Colors.GREEN}[✓] ISP: {Colors.WHITE}{geo.get('isp')}{Colors.END}")
            print(f"{Colors.GREEN}[✓] Timezone: {Colors.WHITE}{geo.get('timezone')}{Colors.END}")
            
            return {
                'ip': ip,
                'city': geo.get('city'),
                'country': geo.get('country'),
                'isp': geo.get('isp')
            }
        else:
            print(f"{Colors.RED}[!] Gagal mendapatkan lokasi{Colors.END}")
            return {'ip': ip}
            
    except Exception as e:
        print(f"{Colors.RED}[!] Gagal verifikasi IP: {e}{Colors.END}")
        return None

def check_whitelist(ip_info):
    """Cek apakah IP terdaftar di whitelist"""
    if not ip_info:
        return False
    
    whitelist_file = os.path.expanduser("~/.duality/whitelist.json")
    os.makedirs(os.path.dirname(whitelist_file), exist_ok=True)
    
    if os.path.exists(whitelist_file):
        with open(whitelist_file, 'r') as f:
            whitelist = json.load(f)
    else:
        whitelist = ["127.0.0.1"]
        with open(whitelist_file, 'w') as f:
            json.dump(whitelist, f, indent=2)
    
    return ip_info['ip'] in whitelist

def add_to_whitelist(ip_info):
    """Tambah IP ke whitelist"""
    if not ip_info:
        return False
    
    whitelist_file = os.path.expanduser("~/.duality/whitelist.json")
    os.makedirs(os.path.dirname(whitelist_file), exist_ok=True)
    
    if os.path.exists(whitelist_file):
        with open(whitelist_file, 'r') as f:
            whitelist = json.load(f)
    else:
        whitelist = []
    
    if ip_info['ip'] not in whitelist:
        whitelist.append(ip_info['ip'])
        with open(whitelist_file, 'w') as f:
            json.dump(whitelist, f, indent=2)
        print(f"{Colors.GREEN}[+] IP {ip_info['ip']} ditambahkan ke whitelist{Colors.END}")
        return True
    else:
        print(f"{Colors.YELLOW}[!] IP {ip_info['ip']} sudah ada di whitelist{Colors.END}")
        return False

def banner():
    """Banner utama DUALITY"""
    logo_path = os.path.join(os.path.dirname(__file__), 'Duality-Attack', 'assets', 'logo.txt')
    
    if os.path.exists(logo_path):
        with open(logo_path, 'r') as f:
            print(f.read())
    else:
        banner_text = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗████████╗██╗   ██╗                 ║
║   ██╔══██╗██║   ██║██╔══██╗██║     ██║╚══██╔══╝╚██╗ ██╔╝                 ║
║   ██║  ██║██║   ██║███████║██║     ██║   ██║    ╚████╔╝                  ║
║   ██║  ██║██║   ██║██╔══██║██║     ██║   ██║     ╚██╔╝                   ║
║   ██████╔╝╚██████╔╝██║  ██║███████╗██║   ██║      ██║                    ║
║   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝                    ║
║                                                                           ║
║   █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗                       ║
║   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝                       ║
║   ███████║   ██║      ██║   ███████║██║     █████╔╝                        ║
║   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗                        ║
║   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗                       ║
║   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
        print(banner_text)
    
    print(f"{Colors.CYAN}{Colors.BOLD}                    DUALITY SECURITY FRAMEWORK{Colors.END}")
    print(f"{Colors.DIM}                  \"The balance between creation and destruction\"{Colors.END}")
    print(f"{Colors.RED}{'═'*71}{Colors.END}")

def show_menu():
    """Menu utama"""
    menu = f"""
{Colors.RED}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────┐{Colors.END}
{Colors.RED}{Colors.BOLD}│                    CHOOSE YOUR PATH                              │{Colors.END}
{Colors.RED}{Colors.BOLD}├─────────────────────────────────────────────────────────────────┤{Colors.END}

{Colors.RED}{Colors.BOLD}   ⚔️  [{Colors.WHITE}1{Colors.RED}]  ATTACK MODE{Colors.END}
{Colors.DIM}       → Penetration testing toolkit{Colors.END}
{Colors.DIM}       → 31 modules: OSINT, Payload, DDoS, Botnet, Exploit{Colors.END}

{Colors.BLUE}{Colors.BOLD}   🛡️  [{Colors.WHITE}2{Colors.BLUE}]  DEFENSE MODE{Colors.END}
{Colors.DIM}       → Security defense toolkit{Colors.END}
{Colors.DIM}       → 15 modules: Firewall, IDS, Honeypot, Backup, Monitor{Colors.END}

{Colors.CYAN}{Colors.BOLD}   ⚡  [{Colors.WHITE}3{Colors.CYAN}]  BATTLE MODE{Colors.END}
{Colors.DIM}       → Attack vs Defense simulation{Colors.END}

{Colors.YELLOW}{Colors.BOLD}   🚪  [{Colors.WHITE}0{Colors.YELLOW}]  EXIT{Colors.END}

{Colors.RED}{Colors.BOLD}└─────────────────────────────────────────────────────────────────┘{Colors.END}
    """
    print(menu)

def launch_attack_mode():
    """Menjalankan Duality Attack"""
    print(f"\n{Colors.YELLOW}[*] Loading attack modules...{Colors.END}")
    loading_animation("Memuat Utility modules", 2, "bar")
    loading_animation("Memuat Attack modules", 2, "bar")
    loading_animation("Memuat Advanced modules", 2, "bar")
    loading_animation("Menjalankan Duality Attack", 2, "bar")
    attack_path = os.path.join(os.path.dirname(__file__), 'Duality-Attack', 'duality.py')
    if os.path.exists(attack_path):
        subprocess.run(['python3', attack_path])
    else:
        print(f"{Colors.RED}[!] Attack mode not found{Colors.END}")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def launch_defense_mode():
    """Menjalankan Duality Defense"""
    print(f"\n{Colors.CYAN}[*] Loading defense modules...{Colors.END}")
    loading_animation("Memuat Firewall modules", 1)
    loading_animation("Memuat IDS modules", 1)
    loading_animation("Memuat Honeypot modules", 1)
    
    defense_path = os.path.join(os.path.dirname(__file__), 'Duality-Defense', 'awakened_core.py')
    if os.path.exists(defense_path):
        subprocess.run(['python3', defense_path])
    else:
        print(f"{Colors.RED}[!] Defense mode not found{Colors.END}")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def launch_battle_mode():
    """Menjalankan Battle Mode"""
    print(f"{Colors.YELLOW}[!] Battle mode coming soon!{Colors.END}")
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.END}")

def main():
    # URUTAN: CEK IP DULU
    ip_info = check_ip()
    
    # Verifikasi IP
    if check_whitelist(ip_info):
        print(f"{Colors.GREEN}[✓] IP terverifikasi!{Colors.END}")
    else:
        print(f"{Colors.RED}[!] IP tidak terdaftar!{Colors.END}")
        print(f"{Colors.YELLOW}[?] Daftarkan IP sekarang? (y/n){Colors.END}")
        reg = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        if reg.lower() == 'y':
            add_to_whitelist(ip_info)
            print(f"{Colors.GREEN}[✓] Silakan restart tools{Colors.END}")
            input(f"\n{Colors.DIM}Press Enter to exit...{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Akses ditolak!{Colors.END}")
            sys.exit(0)
    
    # HABIS ITU MATRIX RAIN
    time.sleep(1)
    matrix_rain_hijau(duration=6, fall_speed=1.5)
    
    # TERUS MASUK MENU
    loading_animation("Initializing DUALITY", 2)
    
    while True:
        clear_screen()
        banner()
        show_menu()
        
        choice = input(f"\n{Colors.RED}┌──({Colors.GREEN}duality{Colors.RED}@{Colors.CYAN}framework{Colors.RED})-{Colors.BLUE}[~]{Colors.RED}\n└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            launch_attack_mode()
        elif choice == '2':
            launch_defense_mode()
        elif choice == '3':
            launch_battle_mode()
        elif choice == '0':
            print(f"\n{Colors.RED}[!] Exiting DUALITY...{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    main()
