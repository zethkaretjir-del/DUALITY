#!/usr/bin/env python3
# FIND COMMAND WRAPPER
# "Cari file dengan kriteria spesifik"

import os
import subprocess
from core.colors import Colors

class FindWrapper:
    def __init__(self):
        self.name = "Find Command Wrapper"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Cari file berdasarkan nama")
        print(f"{Colors.GREEN}[2]{Colors.END} Cari file berdasarkan ukuran")
        print(f"{Colors.GREEN}[3]{Colors.END} Cari file berdasarkan user/group")
        print(f"{Colors.GREEN}[4]{Colors.END} Cari file berdasarkan tipe")
        print(f"{Colors.GREEN}[5]{Colors.END} Cari file yang bisa dieksekusi")
        print(f"{Colors.GREEN}[6]{Colors.END} Advanced search")
        print(f"{Colors.GREEN}[0]{Colors.END} Back")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.search_by_name()
        elif choice == '2':
            self.search_by_size()
        elif choice == '3':
            self.search_by_user_group()
        elif choice == '4':
            self.search_by_type()
        elif choice == '5':
            self.search_executable()
        elif choice == '6':
            self.advanced_search()
    
    def search_by_name(self):
        """Cari file berdasarkan nama"""
        print(f"\n{Colors.CYAN}[*] Cari file berdasarkan nama{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: .) > {Colors.END}") or "."
        name = input(f"{Colors.GREEN}Nama file (bisa pake wildcard *) > {Colors.END}")
        
        cmd = f"find {start_dir} -name '{name}' 2>/dev/null"
        print(f"{Colors.YELLOW}[*] Running: {cmd}{Colors.END}\n")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n')[:50]:
                if line:
                    print(f"  {line}")
            if len(result.stdout.split('\n')) > 50:
                print(f"{Colors.DIM}... dan seterusnya{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada file ditemukan{Colors.END}")
    
    def search_by_size(self):
        """Cari file berdasarkan ukuran"""
        print(f"\n{Colors.CYAN}[*] Cari file berdasarkan ukuran{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: .) > {Colors.END}") or "."
        
        print(f"{Colors.GREEN}[1]{Colors.END} Ukuran exact (bytes)")
        print(f"{Colors.GREEN}[2]{Colors.END} Lebih besar dari")
        print(f"{Colors.GREEN}[3]{Colors.END} Lebih kecil dari")
        size_choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        size = input(f"{Colors.GREEN}Ukuran (bytes) > {Colors.END}")
        
        if size_choice == '1':
            size_opt = f"-size {size}c"
        elif size_choice == '2':
            size_opt = f"-size +{size}c"
        elif size_choice == '3':
            size_opt = f"-size -{size}c"
        else:
            return
        
        cmd = f"find {start_dir} -type f {size_opt} 2>/dev/null"
        print(f"{Colors.YELLOW}[*] Running: {cmd}{Colors.END}\n")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n')[:50]:
                if line:
                    # Dapatkan ukuran file
                    try:
                        size_bytes = os.path.getsize(line) if os.path.exists(line) else 0
                        size_kb = size_bytes / 1024
                        if size_kb < 1024:
                            size_str = f"{size_kb:.1f}KB"
                        else:
                            size_str = f"{size_kb/1024:.1f}MB"
                        print(f"  {line} ({size_str})")
                    except:
                        print(f"  {line}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada file ditemukan{Colors.END}")
    
    def search_by_user_group(self):
        """Cari file berdasarkan user/group"""
        print(f"\n{Colors.CYAN}[*] Cari file berdasarkan user/group{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: /) > {Colors.END}") or "/"
        
        print(f"{Colors.GREEN}[1]{Colors.END} Cari berdasarkan user")
        print(f"{Colors.GREEN}[2]{Colors.END} Cari berdasarkan group")
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            user = input(f"{Colors.GREEN}Username > {Colors.END}")
            cmd = f"find {start_dir} -user {user} 2>/dev/null"
        elif choice == '2':
            group = input(f"{Colors.GREEN}Group name > {Colors.END}")
            cmd = f"find {start_dir} -group {group} 2>/dev/null"
        else:
            return
        
        print(f"{Colors.YELLOW}[*] Running: {cmd}{Colors.END}\n")
        print(f"{Colors.DIM}[*] Ini mungkin butuh waktu lama...{Colors.END}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n')[:50]:
                if line:
                    print(f"  {line}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada file ditemukan{Colors.END}")
    
    def search_by_type(self):
        """Cari file berdasarkan tipe"""
        print(f"\n{Colors.CYAN}[*] Cari file berdasarkan tipe{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: .) > {Colors.END}") or "."
        
        print(f"{Colors.GREEN}[1]{Colors.END} File biasa")
        print(f"{Colors.GREEN}[2]{Colors.END} Directory")
        print(f"{Colors.GREEN}[3]{Colors.END} Symbolic link")
        print(f"{Colors.GREEN}[4]{Colors.END} Socket")
        type_choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        type_map = {'1': 'f', '2': 'd', '3': 'l', '4': 's'}
        file_type = type_map.get(type_choice, 'f')
        
        cmd = f"find {start_dir} -type {file_type} 2>/dev/null | head -50"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n'):
                if line:
                    print(f"  {line}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada ditemukan{Colors.END}")
    
    def search_executable(self):
        """Cari file yang bisa dieksekusi"""
        print(f"\n{Colors.CYAN}[*] Cari file yang bisa dieksekusi{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: .) > {Colors.END}") or "."
        
        cmd = f"find {start_dir} -type f -executable 2>/dev/null | head -50"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n'):
                if line:
                    print(f"  {line}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada file executable ditemukan{Colors.END}")
    
    def advanced_search(self):
        """Advanced search dengan multiple criteria"""
        print(f"\n{Colors.CYAN}[*] Advanced Search{Colors.END}")
        start_dir = input(f"{Colors.GREEN}Directory (default: .) > {Colors.END}") or "."
        
        # Kumpulkan kriteria
        criteria = []
        
        name = input(f"{Colors.GREEN}Nama file (wildcard allowed, kosongkan jika tidak): {Colors.END}")
        if name:
            criteria.append(f"-name '{name}'")
        
        size_input = input(f"{Colors.GREEN}Ukuran (contoh: +1M, -500k, 100c, kosongkan jika tidak): {Colors.END}")
        if size_input:
            criteria.append(f"-size {size_input}")
        
        user = input(f"{Colors.GREEN}User (kosongkan jika tidak): {Colors.END}")
        if user:
            criteria.append(f"-user {user}")
        
        group = input(f"{Colors.GREEN}Group (kosongkan jika tidak): {Colors.END}")
        if group:
            criteria.append(f"-group {group}")
        
        file_type = input(f"{Colors.GREEN}Tipe (f=file, d=dir, l=link, kosongkan jika tidak): {Colors.END}")
        if file_type:
            criteria.append(f"-type {file_type}")
        
        if not criteria:
            print(f"{Colors.RED}[!] Minimal satu kriteria harus diisi!{Colors.END}")
            return
        
        cmd = f"find {start_dir} {' '.join(criteria)} 2>/dev/null | head -50"
        print(f"{Colors.YELLOW}[*] Running: {cmd}{Colors.END}\n")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{Colors.GREEN}[+] Hasil:{Colors.END}")
            for line in result.stdout.split('\n'):
                if line:
                    print(f"  {line}")
        else:
            print(f"{Colors.YELLOW}[!] Tidak ada file ditemukan{Colors.END}")

if __name__ == "__main__":
    finder = FindWrapper()
    finder.run()
