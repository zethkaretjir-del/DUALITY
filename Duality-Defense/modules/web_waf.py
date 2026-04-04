#!/usr/bin/env python3
# WEB APPLICATION FIREWALL - Protect web apps
import re
import time
import threading
from collections import defaultdict

class WebWAF:
    def __init__(self):
        self.blacklist = set()
        self.rate_limit = defaultdict(list)
        self.max_requests = 100
        self.time_window = 60
    
    def detect_sqli(self, payload):
        """Detect SQL injection"""
        sql_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
            r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
            r"w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
            r"(exec|execute|select|insert|update|delete|drop|union|create|alter)"
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                return True
        return False
    
    def detect_xss(self, payload):
        """Detect XSS"""
        xss_patterns = [
            r"<script.*?>.*?</script>",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"onclick=",
            r"<img.*?src=.*?>",
            r"<iframe.*?>"
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, payload, re.IGNORECASE):
                return True
        return False
    
    def check_rate_limit(self, ip):
        """Check rate limit"""
        now = time.time()
        self.rate_limit[ip] = [t for t in self.rate_limit[ip] if now - t < self.time_window]
        
        if len(self.rate_limit[ip]) >= self.max_requests:
            return False
        
        self.rate_limit[ip].append(now)
        return True
    
    def block_ip(self, ip):
        """Block IP address"""
        if ip not in self.blacklist:
            self.blacklist.add(ip)
            print(f"[!] Blocked IP: {ip}")
            # Add to iptables
            os.system(f"iptables -A INPUT -s {ip} -j DROP 2>/dev/null")
    
    def inspect_request(self, ip, method, path, params):
        """Inspect HTTP request"""
        if ip in self.blacklist:
            return False
        
        if not self.check_rate_limit(ip):
            self.block_ip(ip)
            return False
        
        # Check for attacks
        for key, value in params.items():
            if self.detect_sqli(value) or self.detect_xss(value):
                self.block_ip(ip)
                return False
        
        return True

if __name__ == "__main__":
    waf = WebWAF()
    print("[*] Web WAF ready")
