#!/usr/bin/env python3
# AGENT GATEWAY WEB DASHBOARD

import json
import threading
from flask import Flask, render_template_string, jsonify, request
from gateway_core import AgentGateway

app = Flask(__name__)
gateway = AgentGateway()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent Gateway Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0e1a;
            color: #00ff88;
            font-family: monospace;
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
        .agent-list { background: rgba(0,0,0,0.7); border: 1px solid #00ff88; border-radius: 10px; padding: 15px; }
        .agent-item {
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #00ff88;
        }
        .idle { color: #00ff88; }
        .busy { color: #ffaa00; }
        button {
            background: #00ff88;
            color: #0a0e1a;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            margin: 5px;
        }
        input, select {
            background: #0a0e1a;
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 10px;
            margin: 5px;
        }
    </style>
</head>
<body>
    <h1>🚪 AGENT GATEWAY DASHBOARD</h1>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number" id="totalAgents">0</div>
            <div>Total Agents</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="totalTasks">0</div>
            <div>Total Tasks</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="pendingTasks">0</div>
            <div>Pending Tasks</div>
        </div>
    </div>
    
    <div class="agent-list">
        <h2>🤖 Agents</h2>
        <div id="agents"></div>
    </div>
    
    <div style="margin-top: 20px;">
        <h2>📤 Submit Task</h2>
        <select id="agentSelect">
            <option value="">Select Agent</option>
        </select>
        <input type="text" id="taskInput" placeholder="Task command">
        <button onclick="submitTask()">Submit</button>
    </div>
    
    <script>
        function loadData() {
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('totalAgents').innerText = data.total_agents;
                    document.getElementById('totalTasks').innerText = data.total_tasks;
                    document.getElementById('pendingTasks').innerText = data.pending_tasks;
                });
            
            fetch('/api/agents')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    let selectHtml = '<option value="">Select Agent</option>';
                    for(let id in data) {
                        let agent = data[id];
                        html += `<div class="agent-item">
                            <strong>${agent.name}</strong> (${id})<br>
                            Status: <span class="${agent.status}">${agent.status}</span><br>
                            Tasks: ${agent.tasks_completed}
                        </div>`;
                        selectHtml += `<option value="${id}">${agent.name}</option>`;
                    }
                    document.getElementById('agents').innerHTML = html;
                    document.getElementById('agentSelect').innerHTML = selectHtml;
                });
        }
        
        function submitTask() {
            let agentId = document.getElementById('agentSelect').value;
            let task = document.getElementById('taskInput').value;
            
            if(!agentId || !task) return;
            
            fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({agent_id: agentId, task: task})
            }).then(() => {
                document.getElementById('taskInput').value = '';
                loadData();
            });
        }
        
        setInterval(loadData, 2000);
        loadData();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    stats = gateway.get_statistics()
    return jsonify({
        'total_agents': stats['total_agents'],
        'total_tasks': stats['total_tasks'],
        'pending_tasks': stats['pending_tasks']
    })

@app.route('/api/agents')
def get_agents():
    return jsonify(gateway.get_agent_status())

@app.route('/api/submit', methods=['POST'])
def submit_task():
    data = request.json
    agent_id = data.get('agent_id')
    task = data.get('task')
    
    if agent_id and task:
        gateway.submit_task(agent_id, {'command': task})
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error'}), 400

def run_web_server():
    gateway.start_gateway()
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

class GatewayWeb:
    def __init__(self):
        self.name = "Agent Gateway Web"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] Starting Agent Gateway Web Dashboard{Colors.END}")
        print(f"{Colors.GREEN}[+] Web dashboard: http://localhost:5001{Colors.END}")
        run_web_server()

if __name__ == "__main__":
    web = GatewayWeb()
    web.run()
