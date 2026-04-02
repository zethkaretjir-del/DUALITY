#!/usr/bin/env python3
# DUALITY - Main Entry Point
# By: Rian (Gigs) via ZmZ

import os
import sys
import json
from pathlib import Path

# Tambah path core ke sys.path
sys.path.insert(0, str(Path(__file__).parent))

from core.user_manager import UserManager
from core.plugin_manager import PluginManager
from core.report_generator import ReportGenerator
from core.otp_manager import OTPManager

# Warna
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
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║  ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗████████╗██╗   ██╗      ║
║  ██╔══██╗██║   ██║██╔══██╗██║     ██║╚══██╔══╝╚██╗ ██╔╝      ║
║  ██║  ██║██║   ██║███████║██║     ██║   ██║    ╚████╔╝       ║
║  ██║  ██║██║   ██║██╔══██║██║     ██║   ██║     ╚██╔╝        ║
║  ██████╔╝╚██████╔╝██║  ██║███████╗██║   ██║      ██║         ║
║  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝         ║
║                         v2.1 - 49 Modules                    ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.CYAN}{Colors.DIM}                    "Duality - Two Sides of Security"{Colors.END}
    """)

def main_menu(um):
    pm = PluginManager()
    rg = ReportGenerator()
    
    while True:
        clear_screen()
        banner()
        print(f"""
{Colors.GREEN}[1]{Colors.END} Plugin Manager
{Colors.GREEN}[2]{Colors.END} Report Generator
{Colors.GREEN}[3]{Colors.END} View History
{Colors.GREEN}[4]{Colors.END} User Settings
{Colors.RED}[0]{Colors.END} Logout
        """)
        
        choice = input(f"{Colors.YELLOW}[?] Pilih: {Colors.END}")
        
        if choice == '1':
            plugin_menu(pm)
        elif choice == '2':
            report_menu(rg)
        elif choice == '3':
            history_menu(um)
        elif choice == '4':
            user_settings(um)
        elif choice == '0':
            um.logout()
            break
        else:
            print(f"{Colors.RED}❌ Pilihan tidak valid!{Colors.END}")
            input("Tekan Enter...")

def plugin_menu(pm):
    while True:
        clear_screen()
        print(f"""
{Colors.PURPLE}╔══════════════════════════════════════╗
║         PLUGIN MANAGER               ║
╠══════════════════════════════════════╣
║  {Colors.GREEN}[1]{Colors.END} List available plugins      ║
║  {Colors.GREEN}[2]{Colors.END} Load plugin                 ║
║  {Colors.GREEN}[3]{Colors.END} Run plugin                  ║
║  {Colors.GREEN}[4]{Colors.END} List loaded plugins         ║
║  {Colors.GREEN}[5]{Colors.END} Unload plugin               ║
║  {Colors.GREEN}[6]{Colors.END} Show status                 ║
║  {Colors.RED}[0]{Colors.END} Back                          ║
╚══════════════════════════════════════╝
        """)
        
        choice = input(f"{Colors.YELLOW}[?] Pilih: {Colors.END}")
        
        if choice == '1':
            plugins = pm.list_plugins()
            print(f"\n📦 Available plugins: {plugins}")
        elif choice == '2':
            name = input("Nama plugin: ")
            module, msg = pm.load_plugin(name)
            print(f"\n{msg}")
        elif choice == '3':
            name = input("Nama plugin: ")
            if name in pm.list_loaded():
                result, msg = pm.run_plugin(name)
                print(f"\n📤 Result: {result}")
            else:
                print(f"\n❌ Plugin {name} belum diload")
        elif choice == '4':
            loaded = pm.list_loaded()
            print(f"\n🔌 Loaded plugins: {loaded}")
        elif choice == '5':
            name = input("Nama plugin: ")
            success, msg = pm.unload_plugin(name)
            print(f"\n{msg}")
        elif choice == '6':
            pm.show_status()
        elif choice == '0':
            break
        
        input("\nTekan Enter...")

def report_menu(rg):
    while True:
        clear_screen()
        print(f"""
{Colors.PURPLE}╔══════════════════════════════════════╗
║         REPORT GENERATOR              ║
╠══════════════════════════════════════╣
║  {Colors.GREEN}[1]{Colors.END} Generate HTML report        ║
║  {Colors.GREEN}[2]{Colors.END} Generate JSON report        ║
║  {Colors.GREEN}[3]{Colors.END} Generate Text report        ║
║  {Colors.GREEN}[4]{Colors.END} List reports                ║
║  {Colors.RED}[0]{Colors.END} Back                          ║
╚══════════════════════════════════════╝
        """)
        
        choice = input(f"{Colors.YELLOW}[?] Pilih: {Colors.END}")
        
        if choice == '1':
            data = {"scan_result": "example", "status": "success"}
            filepath = rg.generate_html(data)
            print(f"\n✅ Report saved: {filepath}")
        elif choice == '2':
            data = {"scan_result": "example", "status": "success"}
            filepath = rg.generate_json(data)
            print(f"\n✅ Report saved: {filepath}")
        elif choice == '3':
            data = {"scan_result": "example", "status": "success"}
            filepath = rg.generate_text(data)
            print(f"\n✅ Report saved: {filepath}")
        elif choice == '4':
            reports = list(rg.report_dir.glob("*"))
            print("\n📁 Saved reports:")
            for r in reports:
                print(f"  - {r.name} ({r.stat().st_size} bytes)")
        elif choice == '0':
            break
        
        input("\nTekan Enter...")

def history_menu(um):
    clear_screen()
    history = um.get_history()
    print(f"\n{Colors.CYAN}📜 HISTORY:{Colors.END}")
    print("="*50)
    if not history:
        print("Belum ada aktivitas")
    else:
        for h in history:
            print(f"[{h['timestamp']}] {h['action']} - {h['result']}")
    print("="*50)
    input("\nTekan Enter...")

def user_settings(um):
    while True:
        clear_screen()
        print(f"""
{Colors.PURPLE}╔══════════════════════════════════════╗
║         USER SETTINGS                  ║
╠══════════════════════════════════════╣
║  {Colors.GREEN}[1]{Colors.END} Change password            ║
║  {Colors.GREEN}[2]{Colors.END} View profile               ║
║  {Colors.RED}[0]{Colors.END} Back                        ║
╚══════════════════════════════════════╝
        """)
        
        choice = input(f"{Colors.YELLOW}[?] Pilih: {Colors.END}")
        
        if choice == '1':
            old = input("Password lama: ")
            new = input("Password baru: ")
            # Implement change password
            print("\n✅ Password berubah (simulasi)")
        elif choice == '2':
            print(f"\n👤 Username: {um.get_current_user()}")
            print(f"🔑 Role: {um.users.get(um.get_current_user(), {}).get('role', 'user')}")
        elif choice == '0':
            break
        
        input("\nTekan Enter...")

def auth_menu():
    um = UserManager()
    
    while True:
        clear_screen()
        banner()
        print(f"""
{Colors.GREEN}[1]{Colors.END} Login
{Colors.GREEN}[2]{Colors.END} Register
{Colors.RED}[0]{Colors.END} Exit
        """)
        
        choice = input(f"{Colors.YELLOW}[?] Pilih: {Colors.END}")
        
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            success, msg = um.login(username, password)
            print(f"\n{msg}")
            if success:
                input("Tekan Enter...")
                main_menu(um)
                break
        
        elif choice == '2':
            username = input("Username baru: ")
            password = input("Password: ")
            success, msg = um.create_user(username, password)
            print(f"\n{msg}")
            input("Tekan Enter...")
        
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 Bye!{Colors.END}")
            break

if __name__ == "__main__":
    try:
        auth_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Exiting...{Colors.END}")
