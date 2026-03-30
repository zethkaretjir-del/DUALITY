#!/usr/bin/env python3
# DARK WEB MONITORING - Monitor for leaked credentials
import requests
import json
import os
from datetime import datetime

class DarkWebMonitor:
    def __init__(self):
        self.monitor_file = os.path.expanduser("~/.awakened_core/monitored_data.json")
        self.alerts_file = os.path.expanduser("~/.awakened_core/darkweb_alerts.log")
        self.monitored = self.load_monitored()
    
    def load_monitored(self):
        if os.path.exists(self.monitor_file):
            with open(self.monitor_file, 'r') as f:
                return json.load(f)
        return {"emails": [], "domains": []}
    
    def save_monitored(self):
        with open(self.monitor_file, 'w') as f:
            json.dump(self.monitored, f, indent=2)
    
    def add_email(self, email):
        """Add email to monitor"""
        if email not in self.monitored["emails"]:
            self.monitored["emails"].append(email)
            self.save_monitored()
            print(f"[+] Monitoring email: {email}")
    
    def add_domain(self, domain):
        """Add domain to monitor"""
        if domain not in self.monitored["domains"]:
            self.monitored["domains"].append(domain)
            self.save_monitored()
            print(f"[+] Monitoring domain: {domain}")
    
    def check_hibp(self, email):
        """Check Have I Been Pwned API"""
        try:
            headers = {"hibp-api-key": "YOUR_API_KEY"}
            resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
                               headers=headers, timeout=10)
            if resp.status_code == 200:
                breaches = resp.json()
                return breaches
        except:
            pass
        return []
    
    def search_darkweb(self, query):
        """Search dark web (simulated)"""
        # This is a simulation - real dark web monitoring requires special access
        return [
            {"source": "Pastebin", "found": "2024-01-15", "content": f"Credential leak involving {query}"},
            {"source": "Dark Forum", "found": "2024-01-10", "content": f"{query} mentioned in data dump"}
        ]
    
    def monitor(self):
        """Run monitoring"""
        print("[*] Dark Web Monitoring started")
        alerts = []
        
        for email in self.monitored["emails"]:
            breaches = self.check_hibp(email)
            if breaches:
                for breach in breaches:
                    alert = {
                        "type": "email_breach",
                        "data": email,
                        "breach": breach.get("Name"),
                        "date": breach.get("BreachDate"),
                        "timestamp": str(datetime.now())
                    }
                    alerts.append(alert)
                    self.log_alert(alert)
        
        for domain in self.monitored["domains"]:
            results = self.search_darkweb(domain)
            for result in results:
                alert = {
                    "type": "domain_mention",
                    "data": domain,
                    "source": result["source"],
                    "content": result["content"],
                    "timestamp": str(datetime.now())
                }
                alerts.append(alert)
                self.log_alert(alert)
        
        return alerts
    
    def log_alert(self, alert):
        """Log alert to file"""
        with open(self.alerts_file, 'a') as f:
            f.write(f"{json.dumps(alert)}\n")
        print(f"[!] ALERT: {alert}")

if __name__ == "__main__":
    dwm = DarkWebMonitor()
    dwm.add_email("test@example.com")
    dwm.monitor()
