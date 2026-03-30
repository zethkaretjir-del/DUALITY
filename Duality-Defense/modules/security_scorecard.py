#!/usr/bin/env python3
# SECURITY SCORECARD - Nilai keamanan sistem (0-100)
import os
import socket
import psutil
import subprocess

class SecurityScorecard:
    def __init__(self):
        self.score = 100
        self.issues = []
    
    def check_open_ports(self):
        """Check for open ports"""
        open_ports = []
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port < 1024:
                open_ports.append(conn.laddr.port)
        
        if open_ports:
            self.score -= len(open_ports) * 2
            self.issues.append(f"Open privileged ports: {open_ports}")
    
    def check_firewall(self):
        """Check if firewall is active"""
        result = subprocess.run(['iptables', '-L'], capture_output=True, text=True)
        if "Chain INPUT (policy ACCEPT)" in result.stdout:
            self.score -= 20
            self.issues.append("Firewall not configured (default ACCEPT)")
    
    def check_fail2ban(self):
        """Check if fail2ban is running"""
        result = subprocess.run(['pgrep', 'fail2ban'], capture_output=True)
        if result.returncode != 0:
            self.score -= 15
            self.issues.append("Fail2ban not running")
    
    def check_ssh_config(self):
        """Check SSH security"""
        if os.path.exists("/etc/ssh/sshd_config"):
            with open("/etc/ssh/sshd_config", 'r') as f:
                config = f.read()
                if "PermitRootLogin yes" in config:
                    self.score -= 10
                    self.issues.append("SSH root login enabled")
                if "PasswordAuthentication yes" in config:
                    self.score -= 5
                    self.issues.append("SSH password authentication enabled")
    
    def check_updates(self):
        """Check for system updates"""
        try:
            result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)
            updates = len([l for l in result.stdout.split('\n') if 'upgradable' in l])
            if updates > 0:
                self.score -= min(updates, 30)
                self.issues.append(f"{updates} packages need update")
        except:
            pass
    
    def run_audit(self):
        """Run all checks"""
        self.check_open_ports()
        self.check_firewall()
        self.check_fail2ban()
        self.check_ssh_config()
        self.check_updates()
        
        return {
            "score": max(0, self.score),
            "issues": self.issues,
            "grade": self.get_grade()
        }
    
    def get_grade(self):
        if self.score >= 90:
            return "A+ (Excellent)"
        elif self.score >= 80:
            return "A (Very Good)"
        elif self.score >= 70:
            return "B (Good)"
        elif self.score >= 60:
            return "C (Fair)"
        elif self.score >= 50:
            return "D (Poor)"
        else:
            return "F (Critical)"

if __name__ == "__main__":
    sc = SecurityScorecard()
    result = sc.run_audit()
    print(f"Security Score: {result['score']}/100 ({result['grade']})")
    for issue in result['issues']:
        print(f"  - {issue}")
