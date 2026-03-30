#!/usr/bin/env python3
# FORENSIC ANALYSIS - Analyze system after attack
import os
import json
import subprocess
from datetime import datetime

class ForensicAnalysis:
    def __init__(self):
        self.report_dir = os.path.expanduser("~/.awakened_core/forensics")
        os.makedirs(self.report_dir, exist_ok=True)
    
    def collect_logs(self):
        """Collect system logs"""
        logs = {}
        log_files = [
            "/var/log/auth.log",
            "/var/log/syslog",
            "/var/log/kern.log",
            "/data/data/com.termux/files/usr/var/log/auth.log"
        ]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs[log_file] = f.read()[-10000:]  # Last 10000 lines
        
        return logs
    
    def collect_network(self):
        """Collect network information"""
        network = {
            "connections": [],
            "open_ports": []
        }
        
        # Get active connections
        result = subprocess.run(['netstat', '-tun'], capture_output=True, text=True)
        network["connections"] = result.stdout.split('\n')
        
        # Get listening ports
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                network["open_ports"].append(conn.laddr.port)
        
        return network
    
    def collect_processes(self):
        """Collect running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                processes.append(proc.info)
            except:
                pass
        return processes
    
    def collect_files(self, directory):
        """Collect suspicious files"""
        suspicious_files = []
        patterns = ['reverse_shell', 'keylogger', 'ransomware', 'backdoor', '.enc', '.crypted']
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(p in file.lower() for p in patterns):
                    suspicious_files.append(os.path.join(root, file))
        
        return suspicious_files
    
    def generate_timeline(self):
        """Generate attack timeline"""
        timeline = []
        # Parse logs for timeline
        auth_log = "/var/log/auth.log"
        if os.path.exists(auth_log):
            with open(auth_log, 'r') as f:
                for line in f:
                    if 'Failed password' in line or 'Accepted' in line or 'BREAK-IN' in line:
                        timeline.append(line.strip())
        return timeline
    
    def create_report(self):
        """Create forensic report"""
        report = {
            "timestamp": str(datetime.now()),
            "logs": self.collect_logs(),
            "network": self.collect_network(),
            "processes": self.collect_processes(),
            "timeline": self.generate_timeline(),
            "suspicious_files": self.collect_files(os.path.expanduser("~"))
        }
        
        filename = f"{self.report_dir}/forensic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[+] Forensic report saved: {filename}")
        return report

if __name__ == "__main__":
    fa = ForensicAnalysis()
    fa.create_report()
