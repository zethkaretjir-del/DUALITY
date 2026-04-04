#!/usr/bin/env python3
import os
import sys
import time
import random

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

def logo_duality():
    """Logo DUALITY"""
    logo = f"""
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
{Colors.CYAN}{Colors.BOLD}                    DUALITY SECURITY FRAMEWORK{Colors.END}
{Colors.DIM}                  \"The balance between creation and destruction\"{Colors.END}
"""
    print(logo)

def progress_bar(current, total, width=50):
    """Tampilkan progress bar"""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    
    # Warna berdasarkan persen
    if percent < 0.3:
        color = Colors.RED
    elif percent < 0.7:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    
    print(f"\r{color}[{bar}]{Colors.END} {percent*100:.1f}%", end="", flush=True)

def install_animation():
    """Animasi install dengan progress bar"""
    clear_screen()
    
    # Tampilkan logo dulu
    logo_duality()
    print(f"\n{Colors.CYAN}{'='*71}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}📦 INSTALLING DUALITY FRAMEWORK{Colors.END}")
    print(f"{Colors.CYAN}{'='*71}{Colors.END}\n")
    
    # Steps instalasi
    steps = [
        ("Memeriksa sistem...", 5),
        ("Menginstall dependencies...", 10),
        ("Menginstall Python packages...", 15),
        ("Menginstall OSINT modules...", 10),
        ("Menginstall Attack modules...", 10),
        ("Menginstall Utility modules...", 10),
        ("Menginstall Advanced modules...", 10),
        ("Menginstall Botnet modules...", 10),
        ("Menginstall Web Panel...", 10),
        ("Konfigurasi sistem...", 5),
        ("Finalisasi instalasi...", 5),
    ]
    
    total_weight = sum(weight for _, weight in steps)
    current_progress = 0
    
    for step, weight in steps:
        print(f"{Colors.CYAN}[*]{Colors.END} {step}", end=" ")
        
        # Simulasi proses
        for i in range(weight):
            time.sleep(random.uniform(0.1, 0.3))
            current_progress += 1
            progress_bar(current_progress, total_weight)
        
        print(f" {Colors.GREEN}✓{Colors.END}")
    
    print(f"\n\n{Colors.GREEN}{'═'*71}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ INSTALLATION COMPLETE!{Colors.END}")
    print(f"{Colors.GREEN}{'═'*71}{Colors.END}")
    
    time.sleep(1)
    
    # Tampilkan summary
    print(f"""
{Colors.CYAN}📊 INSTALLATION SUMMARY:{Colors.END}
  {Colors.GREEN}✓{Colors.END} Dependencies installed
  {Colors.GREEN}✓{Colors.END} 31 modules loaded
  {Colors.GREEN}✓{Colors.END} Web panel configured
  {Colors.GREEN}✓{Colors.END} Botnet C2 ready
  {Colors.GREEN}✓{Colors.END} Discord/Telegram bots ready

{Colors.YELLOW}🚀 DUALITY is ready to use!{Colors.END}
    """)
    
    time.sleep(2)

def install_with_matrix():
    """Installasi dengan efek Matrix rain"""
    clear_screen()
    
    # Matrix rain dulu
    print(f"{Colors.GREEN}[*] Initializing installation...{Colors.END}")
    time.sleep(1)
    
    # Animasi matrix rain sederhana
    for _ in range(20):
        line = ""
        for _ in range(60):
            line += random.choice("01")
        print(f"\r{Colors.GREEN}{line}{Colors.END}", end="")
        time.sleep(0.05)
    
    print("\n")
    
    # Install animation
    install_animation()
    
    # Matrix rain lagi di akhir
    print(f"\n{Colors.GREEN}[*] Finalizing...{Colors.END}")
    for _ in range(15):
        line = ""
        for _ in range(60):
            line += random.choice("01")
        print(f"\r{Colors.GREEN}{line}{Colors.END}", end="")
        time.sleep(0.05)
    
    print("\n")
    print(f"{Colors.GREEN}{Colors.BOLD}✨ DUALITY INSTALLED SUCCESSFULLY! ✨{Colors.END}")

def loading_with_logo(duration=3):
    """Loading dengan logo DUALITY"""
    clear_screen()
    logo_duality()
    
    print(f"\n{Colors.CYAN}{'═'*71}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}⚡ LOADING DUALITY{Colors.END}")
    print(f"{Colors.CYAN}{'═'*71}{Colors.END}\n")
    
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(duration * 10):
        print(f"\r{Colors.GREEN}Initializing modules {spinner[i % len(spinner)]}{Colors.END}", end="", flush=True)
        time.sleep(0.1)
    
    print(f"\r{Colors.GREEN}Initializing modules ✅ Done!{Colors.END}")
    time.sleep(0.5)

if __name__ == "__main__":
    # Pilih mode
    print("Pilih mode:")
    print("[1] Install Animation (Progress Bar)")
    print("[2] Loading with Logo")
    print("[3] Full Install with Matrix")
    
    choice = input("\nPilih (1-3): ")
    
    if choice == '1':
        install_animation()
    elif choice == '2':
        loading_with_logo(3)
    elif choice == '3':
        install_with_matrix()
    else:
        install_animation()
