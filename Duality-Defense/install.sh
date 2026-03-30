#!/bin/bash
echo "🛡️ AWAKENED CORE - Defense Toolkit Installer"
echo "============================================"

if command -v pkg &> /dev/null; then
    echo "[*] Detected: Termux"
    pkg update -y
    pkg install python -y
elif command -v apt &> /dev/null; then
    echo "[*] Detected: Linux"
    sudo apt update -y
    sudo apt install python3 python3-pip -y
fi

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

echo "[+] Installation complete!"
echo "[*] Run: python3 awakened_core.py"
