#!/usr/bin/env python3
# MEMORY FORENSICS - Analisis memory dump tanpa debug symbols
# Referensi: mquire - Linux memory forensics tanpa debug symbols

import os
import sys
import subprocess
import json
import tempfile
from datetime import datetime
from core.colors import Colors

class MemoryForensics:
    def __init__(self):
        self.name = "Memory Forensics"
        self.tools = {
            'avml': 'https://github.com/microsoft/avml/releases',
            'volatility3': 'https://github.com/volatilityfoundation/volatility3'
        }
    
    def check_tools(self):
        """Cek tools yang diperlukan"""
        missing = []
        # Cek volatility3
        if subprocess.run(['which', 'vol'], capture_output=True).returncode != 0:
            missing.append('volatility3')
        # Cek avml
        if subprocess.run(['which', 'avml'], capture_output=True).returncode != 0:
            missing.append('avml')
        return missing
    
    def capture_memory(self, output_file=None):
        """Capture memory dump dari sistem"""
        print(f"{Colors.CYAN}[*] Capturing memory...{Colors.END}")
        
        if output_file is None:
            output_file = f"/tmp/memory_dump_{int(time.time())}.lime"
        
        # Coba pake avml (Linux)
        try:
            subprocess.run(['sudo', 'avml', output_file], timeout=60)
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024**3)
                print(f"{Colors.GREEN}[+] Memory captured: {output_file} ({size:.2f} GB){Colors.END}")
                return output_file
        except:
            pass
        
        # Fallback: pake /proc/kcore (limited)
        try:
            subprocess.run(['dd', 'if=/proc/kcore', f'of={output_file}', 'bs=1M'], timeout=30)
            if os.path.exists(output_file):
                print(f"{Colors.YELLOW}[!] Limited capture via /proc/kcore{Colors.END}")
                return output_file
        except:
            pass
        
        print(f"{Colors.RED}[!] Failed to capture memory{Colors.END}")
        return None
    
    def analyze_processes(self, dump_file):
        """Analisis proses dari memory dump"""
        print(f"{Colors.CYAN}[*] Analyzing processes...{Colors.END}")
        
        processes = []
        try:
            # Pake strings untuk extract proses
            result = subprocess.run(['strings', dump_file], capture_output=True, text=True, timeout=60)
            lines = result.stdout.split('\n')
            
            # Cari pola proses
            import re
            pattern = r'/([a-zA-Z0-9_\-\.]+)$'
            for line in lines:
                if line.startswith('/') and 'bin' in line:
                    match = re.search(pattern, line)
                    if match:
                        proc = match.group(1)
                        if proc not in processes and len(proc) > 2:
                            processes.append(proc)
        except:
            pass
        
        return processes[:50]  # Limit 50 proses
    
    def analyze_network(self, dump_file):
        """Analisis koneksi jaringan dari memory dump"""
        print(f"{Colors.CYAN}[*] Analyzing network connections...{Colors.END}")
        
        connections = []
        try:
            result = subprocess.run(['strings', dump_file], capture_output=True, text=True, timeout=60)
            
            import re
            # Cari IP addresses
            ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            ips = re.findall(ip_pattern, result.stdout)
            connections = list(set(ips))[:20]
        except:
            pass
        
        return connections
    
    def analyze_files(self, dump_file):
        """Analisis file yang terbuka dari memory dump"""
        print(f"{Colors.CYAN}[*] Analyzing open files...{Colors.END}")
        
        files = []
        try:
            result = subprocess.run(['strings', dump_file], capture_output=True, text=True, timeout=60)
            
            for line in result.stdout.split('\n'):
                if line.startswith('/') and (line.endswith('.py') or line.endswith('.sh') or line.endswith('.conf')):
                    if line not in files:
                        files.append(line)
        except:
            pass
        
        return files[:30]
    
    def detect_suspicious(self, processes, connections, files):
        """Deteksi aktivitas mencurigakan"""
        suspicious = []
        
        # Proses mencurigakan
        suspicious_procs = ['nc', 'ncat', 'reverse', 'shell', 'meterpreter', 'msf']
        for proc in processes:
            for sp in suspicious_procs:
                if sp in proc.lower():
                    suspicious.append({
                        'type': 'suspicious_process',
                        'name': proc,
                        'reason': f'Process name contains "{sp}"'
                    })
        
        # Koneksi mencurigakan
        suspicious_ports = ['4444', '1337', '31337', '5555', '8080']
        for conn in connections:
            for port in suspicious_ports:
                if f':{port}' in conn or conn.endswith(port):
                    suspicious.append({
                        'type': 'suspicious_connection',
                        'ip': conn,
                        'reason': f'Connection on suspicious port {port}'
                    })
        
        return suspicious
    
    def generate_report(self, dump_file, processes, connections, files, suspicious):
        """Generate laporan forensik"""
        report = {
            'timestamp': str(datetime.now()),
            'dump_file': dump_file,
            'processes': processes,
            'network_connections': connections,
            'open_files': files,
            'suspicious_activities': suspicious
        }
        
        filename = f"forensics_report_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename
    
    def run(self):
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       🔍 MEMORY FORENSICS{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Capture Memory Dump")
        print(f"{Colors.GREEN}[2]{Colors.END} Analyze Existing Dump")
        print(f"{Colors.GREEN}[3]{Colors.END} Install Dependencies")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            output = input(f"{Colors.GREEN}Output file (default: /tmp/memory_dump.lime) > {Colors.END}")
            if not output:
                output = None
            dump_file = self.capture_memory(output)
            
            if dump_file:
                print(f"\n{Colors.CYAN}[*] Analyzing dump...{Colors.END}")
                processes = self.analyze_processes(dump_file)
                connections = self.analyze_network(dump_file)
                files = self.analyze_files(dump_file)
                suspicious = self.detect_suspicious(processes, connections, files)
                
                print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
                print(f"{Colors.BOLD}📊 ANALYSIS RESULTS{Colors.END}")
                print(f"{Colors.GREEN}{'='*55}{Colors.END}")
                print(f"{Colors.CYAN}Processes found: {len(processes)}{Colors.END}")
                print(f"{Colors.CYAN}Network connections: {len(connections)}{Colors.END}")
                print(f"{Colors.CYAN}Open files: {len(files)}{Colors.END}")
                
                if suspicious:
                    print(f"\n{Colors.RED}[!] Suspicious activities detected!{Colors.END}")
                    for s in suspicious[:10]:
                        print(f"  {s['type']}: {s.get('name', s.get('ip', 'N/A'))}")
                
                report_file = self.generate_report(dump_file, processes, connections, files, suspicious)
                print(f"\n{Colors.GREEN}[+] Report saved: {report_file}{Colors.END}")
        
        elif choice == '2':
            dump_file = input(f"{Colors.GREEN}Dump file path > {Colors.END}")
            if os.path.exists(dump_file):
                processes = self.analyze_processes(dump_file)
                connections = self.analyze_network(dump_file)
                files = self.analyze_files(dump_file)
                suspicious = self.detect_suspicious(processes, connections, files)
                
                print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
                print(f"{Colors.BOLD}📊 ANALYSIS RESULTS{Colors.END}")
                print(f"{Colors.GREEN}{'='*55}{Colors.END}")
                print(f"{Colors.CYAN}Processes: {len(processes)}{Colors.END}")
                print(f"{Colors.CYAN}Network: {len(connections)}{Colors.END}")
                print(f"{Colors.CYAN}Files: {len(files)}{Colors.END}")
                if suspicious:
                    print(f"{Colors.RED}[!] Suspicious: {len(suspicious)}{Colors.END}")
                
                report_file = self.generate_report(dump_file, processes, connections, files, suspicious)
                print(f"{Colors.GREEN}[+] Report saved: {report_file}{Colors.END}")
        
        elif choice == '3':
            print(f"{Colors.CYAN}[*] Installing volatility3...{Colors.END}")
            os.system('pip install volatility3')
            print(f"{Colors.CYAN}[*] Installing avml...{Colors.END}")
            print(f"{Colors.YELLOW}[!] Manual install: {self.tools['avml']}{Colors.END}")

if __name__ == "__main__":
    import time
    tool = MemoryForensics()
    tool.run()
