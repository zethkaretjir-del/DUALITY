#!/usr/bin/env python3
# AI DATA SECURITY - Protect sensitive data from AI/LLM

import re
import json
import hashlib
import os
from datetime import datetime
from core.colors import Colors

class AIDataSecurity:
    def __init__(self):
        self.name = "AI Data Security"
        self.data_dir = os.path.expanduser("~/.duality/security")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Detection patterns
        self.patterns = {
            'email': {
                'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                'name': 'Email Address',
                'risk': 'HIGH'
            },
            'phone': {
                'pattern': r'(\+62|0)[0-9]{9,12}',
                'name': 'Phone Number',
                'risk': 'HIGH'
            },
            'credit_card': {
                'pattern': r'\b(?:\d[ -]*?){13,16}\b',
                'name': 'Credit Card Number',
                'risk': 'CRITICAL'
            },
            'api_key': {
                'pattern': r'(api[_-]?key|apikey|token)[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9]{16,64})',
                'name': 'API Key',
                'risk': 'CRITICAL'
            },
            'password': {
                'pattern': r'(password|passwd|pwd)[\s]*[:=][\s]*[\'"]?([^\s]{4,})',
                'name': 'Password',
                'risk': 'CRITICAL'
            },
            'ip_address': {
                'pattern': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                'name': 'IP Address',
                'risk': 'MEDIUM'
            },
            'jwt_token': {
                'pattern': r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
                'name': 'JWT Token',
                'risk': 'CRITICAL'
            },
            'ssn': {
                'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
                'name': 'SSN (US)',
                'risk': 'CRITICAL'
            },
            'bank_account': {
                'pattern': r'\b\d{10,16}\b',
                'name': 'Bank Account',
                'risk': 'HIGH'
            },
            'secret_key': {
                'pattern': r'(secret|private_key|rsa|ec_key)[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9+/=]{32,})',
                'name': 'Secret Key',
                'risk': 'CRITICAL'
            }
        }
        
        # Redaction methods
        self.redaction_methods = {
            'mask': self.mask_redact,
            'encrypt': self.encrypt_redact,
            'hash': self.hash_redact,
            'remove': self.remove_redact
        }
    
    def detect_sensitive_data(self, text):
        """Detect sensitive data in text"""
        findings = []
        
        for data_type, info in self.patterns.items():
            matches = re.findall(info['pattern'], text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else str(match)
                else:
                    match = str(match)
                
                findings.append({
                    'type': data_type,
                    'name': info['name'],
                    'value': match,
                    'risk': info['risk'],
                    'position': text.find(match)
                })
        
        return findings
    
    def mask_redact(self, text, pattern):
        """Mask sensitive data (***)"""
        return re.sub(pattern, '[REDACTED]', text)
    
    def encrypt_redact(self, text, pattern):
        """Encrypt sensitive data (AES-256)"""
        from cryptography.fernet import Fernet
        
        key_file = f"{self.data_dir}/encryption_key.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        
        cipher = Fernet(key)
        
        def encrypt_match(match):
            encrypted = cipher.encrypt(match.group(0).encode())
            return f"[ENCRYPTED:{encrypted[:20].decode('utf-8', errors='ignore')}...]"
        
        return re.sub(pattern, encrypt_match, text)
    
    def hash_redact(self, text, pattern):
        """Hash sensitive data (SHA256)"""
        def hash_match(match):
            hashed = hashlib.sha256(match.group(0).encode()).hexdigest()[:16]
            return f"[HASH:{hashed}]"
        
        return re.sub(pattern, hash_match, text)
    
    def remove_redact(self, text, pattern):
        """Remove sensitive data completely"""
        return re.sub(pattern, '', text)
    
    def redact_data(self, text, method='mask'):
        """Redact sensitive data using selected method"""
        if method not in self.redaction_methods:
            method = 'mask'
        
        redacted_text = text
        findings = self.detect_sensitive_data(text)
        
        for data_type, info in self.patterns.items():
            redacted_text = self.redaction_methods[method](redacted_text, info['pattern'])
        
        return redacted_text, findings
    
    def scan_file(self, filepath, method='mask'):
        """Scan and redact file"""
        if not os.path.exists(filepath):
            return None, []
        
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()
        
        redacted_content, findings = self.redact_data(content, method)
        
        # Save redacted version
        output_path = f"{filepath}.redacted"
        with open(output_path, 'w') as f:
            f.write(redacted_content)
        
        return output_path, findings
    
    def generate_report(self, findings):
        """Generate security report"""
        report = {
            'timestamp': str(datetime.now()),
            'total_findings': len(findings),
            'risk_breakdown': {},
            'findings': findings
        }
        
        for finding in findings:
            risk = finding['risk']
            if risk not in report['risk_breakdown']:
                report['risk_breakdown'][risk] = 0
            report['risk_breakdown'][risk] += 1
        
        return report
    
    def show_report(self, findings):
        """Display security report"""
        report = self.generate_report(findings)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}🛡️ AI DATA SECURITY REPORT{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.WHITE}  Total Sensitive Data: {report['total_findings']}{Colors.END}")
        
        print(f"\n{Colors.CYAN}Risk Breakdown:{Colors.END}")
        for risk, count in report['risk_breakdown'].items():
            color = Colors.RED if risk == 'CRITICAL' else Colors.YELLOW if risk == 'HIGH' else Colors.CYAN
            print(f"  {color}{risk}: {count}{Colors.END}")
        
        if findings:
            print(f"\n{Colors.YELLOW}Sample Findings:{Colors.END}")
            for f in findings[:10]:
                risk_color = Colors.RED if f['risk'] == 'CRITICAL' else Colors.YELLOW
                print(f"  {risk_color}[{f['name']}]{Colors.END} {f['value'][:50]}... ({f['risk']})")
    
    def run(self):
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       🛡️ AI DATA SECURITY{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Scan Text")
        print(f"{Colors.GREEN}[2]{Colors.END} Scan File")
        print(f"{Colors.GREEN}[3]{Colors.END} Scan Clipboard")
        print(f"{Colors.GREEN}[4]{Colors.END} Redaction Methods")
        print(f"{Colors.GREEN}[5]{Colors.END} Real-time Monitor")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            text = input(f"{Colors.GREEN}Text to scan > {Colors.END}")
            method = input(f"{Colors.GREEN}Redaction method (mask/encrypt/hash/remove) > {Colors.END}") or "mask"
            
            redacted, findings = self.redact_data(text, method)
            self.show_report(findings)
            
            if findings:
                print(f"\n{Colors.CYAN}Original:{Colors.END}\n{text[:200]}")
                print(f"\n{Colors.GREEN}Redacted:{Colors.END}\n{redacted[:200]}")
        
        elif choice == '2':
            filepath = input(f"{Colors.GREEN}File path > {Colors.END}")
            method = input(f"{Colors.GREEN}Redaction method > {Colors.END}") or "mask"
            
            output, findings = self.scan_file(filepath, method)
            self.show_report(findings)
            
            if output:
                print(f"{Colors.GREEN}[+] Redacted file saved: {output}{Colors.END}")
        
        elif choice == '3':
            try:
                import subprocess
                result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
                clipboard = result.stdout.strip()
                if clipboard:
                    redacted, findings = self.redact_data(clipboard, 'mask')
                    self.show_report(findings)
                    print(f"\n{Colors.CYAN}Clipboard content (redacted):{Colors.END}\n{redacted[:500]}")
                else:
                    print(f"{Colors.YELLOW}[!] Clipboard empty{Colors.END}")
            except:
                print(f"{Colors.RED}[!] termux-clipboard-get not available{Colors.END}")
        
        elif choice == '4':
            print(f"\n{Colors.CYAN}Redaction Methods:{Colors.END}")
            print(f"  {Colors.GREEN}mask{Colors.END} - Replace with [REDACTED]")
            print(f"  {Colors.GREEN}encrypt{Colors.END} - AES-256 encryption")
            print(f"  {Colors.GREEN}hash{Colors.END} - SHA256 hash")
            print(f"  {Colors.GREEN}remove{Colors.END} - Remove completely")
        
        elif choice == '5':
            print(f"{Colors.CYAN}[*] Real-time monitor started{Colors.END}")
            print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}")
            
            try:
                import subprocess
                while True:
                    result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
                    clipboard = result.stdout.strip()
                    if clipboard:
                        findings = self.detect_sensitive_data(clipboard)
                        if findings:
                            print(f"\n{Colors.RED}[!] Sensitive data detected in clipboard!{Colors.END}")
                            self.show_report(findings)
                    time.sleep(2)
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}[+] Monitor stopped{Colors.END}")

if __name__ == "__main__":
    import time
    security = AIDataSecurity()
    security.run()
