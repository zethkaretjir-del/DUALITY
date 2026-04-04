#!/usr/bin/env python3
# DUALITY LAUNCHER - FIXED VERSION
# "Clean, Simple, and Works"

import os
import sys
import time
import random
import json
import subprocess
import requests

# ========== WARNA ==========
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

# ========== FUNGSI UTILITY ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading_animation(text="Loading", duration=2):
    """Simple loading animation"""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    for i in range(duration * 10):
        print(f"\r{text} {chars[i % len(chars)]}", end="")
        time.sleep(0.1)
    print()

# ========== MATRIX RAIN ==========
def matrix_rain(duration=5):
    """Matrix rain animation"""
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24

    chars = "01アイウエオカキクケコサシスセソタチツテト"
    GREEN_BRIGHT = '\033[92m'
    GREEN_DARK = '\033[32m'

    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.2, 0.5),
            'length': random.randint(5, 15)
        })

    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            frame = [[' ' for _ in range(columns)] for _ in range(rows)]
            for x in range(columns):
                data = columns_data[x]
                data['y'] += data['speed']
                if data['y'] > rows + data['length']:
                    data['y'] = -data['length']
                    data['speed'] = random.uniform(0.2, 0.5)
                    data['length'] = random.randint(5, 15)

                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        char = random.choice(chars)
                        if i == 0:
                            frame[y][x] = f"{GREEN_BRIGHT}{char}{Colors.END}"
                        else:
                            frame[y][x] = f"{GREEN_DARK}{char}{Colors.END}"

            output = []
            for y in range(rows):
                output.append(''.join(frame[y]))
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(output))
            sys.stdout.flush()
            time.sleep(0.03)
    except:
        pass
    print(Colors.END)

# ========== IP & WHITELIST ==========
def get_whitelist_file():
    return os.path.expanduser("~/.duality/whitelist.json")

def check_ip():
    """Cek IP publik dan lokasi"""
    print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
    print(f"{Colors.BOLD}🔍 VERIFIKASI SISTEM{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}\n")

    try:
        print(f"{Colors.YELLOW}[*] Mengecek IP publik...{Colors.END}")
        ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"{Colors.GREEN}[✓] IP Publik: {Colors.WHITE}{ip}{Colors.END}")

        geo = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        if geo.get('status') == 'success':
            print(f"{Colors.GREEN}[✓] Lokasi: {Colors.WHITE}{geo.get('city')}, {geo.get('country')}{Colors.END}")
            print(f"{Colors.GREEN}[✓] ISP: {Colors.WHITE}{geo.get('isp')}{Colors.END}\n")
            return {'ip': ip, 'city': geo.get('city'), 'country': geo.get('country'), 'isp': geo.get('isp')}
        else:
            print(f"{Colors.RED}[!] Gagal dapat lokasi{Colors.END}\n")
            return {'ip': ip}
    except Exception as e:
        print(f"{Colors.RED}[!] Gagal verifikasi: {e}{Colors.END}\n")
        return None

def is_whitelisted(ip_info):
    if not ip_info:
        return False
    whitelist_file = get_whitelist_file()
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
    if not ip_info:
        return False
    whitelist_file = get_whitelist_file()
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
        print(f"{Colors.GREEN}[✓] IP {ip_info['ip']} ditambahkan ke whitelist{Colors.END}")
        return True
    else:
        print(f"{Colors.YELLOW}[!] IP sudah terdaftar{Colors.END}")
        return False

# ========== BANNER & MENU ==========
def banner():
    print(f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║   ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗████████╗██╗   ██╗     ║
║   ██╔══██╗██║   ██║██╔══██╗██║     ██║╚══██╔══╝╚██╗ ██╔╝     ║
║   ██║  ██║██║   ██║███████║██║     ██║   ██║    ╚████╔╝      ║
║   ██║  ██║██║   ██║██╔══██║██║     ██║   ██║     ╚██╔╝       ║
║   ██████╔╝╚██████╔╝██║  ██║███████╗██║   ██║      ██║        ║
║   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝        ║
║                         v2.1 - 49 Modules                    ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.CYAN}                    \"The balance between creation and destruction\"{Colors.END}
    """)

def show_menu():
    print(f"""
{Colors.RED}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────┐{Colors.END}
{Colors.RED}{Colors.BOLD}│                    CHOOSE YOUR PATH                              │{Colors.END}
{Colors.RED}{Colors.BOLD}├─────────────────────────────────────────────────────────────────┤{Colors.END}

{Colors.RED}{Colors.BOLD}   ⚔️  [{Colors.WHITE}1{Colors.RED}]  ATTACK MODE{Colors.END}
{Colors.DIM}       → Penetration testing toolkit (31 modules){Colors.END}

{Colors.BLUE}{Colors.BOLD}   🛡️  [{Colors.WHITE}2{Colors.BLUE}]  DEFENSE MODE{Colors.END}
{Colors.DIM}       → Security defense toolkit (15 modules){Colors.END}

{Colors.YELLOW}{Colors.BOLD}   🚪  [{Colors.WHITE}0{Colors.YELLOW}]  EXIT{Colors.END}

{Colors.RED}{Colors.BOLD}└─────────────────────────────────────────────────────────────────┘{Colors.END}
    """)

# ========== LAUNCHER ==========
def launch_attack_mode():
    attack_path = os.path.join(os.path.dirname(__file__), 'Duality-Attack', 'duality.py')
    if os.path.exists(attack_path):
        loading_animation("Loading Attack Modules", 4)
        subprocess.run(['python3', attack_path])
    else:
        print(f"{Colors.RED}[!] Attack mode not found at: {attack_path}{Colors.END}")
        input("Press Enter to continue...")

def launch_defense_mode():
    defense_path = os.path.join(os.path.dirname(__file__), 'Duality-Defense', 'awakened_core.py')
    if os.path.exists(defense_path):
        loading_animation("Loading Defense Modules", 1)
        subprocess.run(['python3', defense_path])
    else:
        print(f"{Colors.RED}[!] Defense mode not found at: {defense_path}{Colors.END}")
        input("Press Enter to continue...")

# ========== MAIN ==========
def main():
    # 1. Cek IP & Whitelist
    ip_info = check_ip()
    if ip_info and is_whitelisted(ip_info):
        print(f"{Colors.GREEN}[✓] IP terverifikasi!{Colors.END}")
    else:
        print(f"{Colors.RED}[!] IP tidak terdaftar!{Colors.END}")
        print(f"{Colors.YELLOW}[?] Daftarkan IP sekarang? (y/n){Colors.END}")
        reg = input(f"{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        if reg.lower() == 'y':
            add_to_whitelist(ip_info)
            print(f"{Colors.GREEN}[✓] Silakan restart tools{Colors.END}")
            input("Press Enter to exit...")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Akses ditolak!{Colors.END}")
            sys.exit(0)

    # 2. Matrix Rain
    time.sleep(1)
    matrix_rain(4)

    # 3. Banner & Menu
    loading_animation("Loading DUALITY Framework", 1)
    clear_screen()
    banner()

    while True:
        show_menu()
        choice = input(f"\n{Colors.RED}┌──({Colors.GREEN}duality{Colors.RED}@{Colors.CYAN}framework{Colors.RED})-{Colors.BLUE}[~]{Colors.RED}\n└─{Colors.WHITE}$ {Colors.END}")

        if choice == '1':
            launch_attack_mode()
        elif choice == '2':
            launch_defense_mode()
        elif choice == '0':
            print(f"\n{Colors.RED}[!] Exiting DUALITY...{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
        sys.exit(0)
