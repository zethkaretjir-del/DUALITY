#!/bin/bash
echo "🔥 FORGOTTEN CORE v3.0 INSTALLER 🔥"
if command -v pkg &> /dev/null; then
    pkg update -y
    pkg install python tor termux-api -y
else
    sudo apt update -y
    sudo apt install python3 python3-pip tor -y
fi
pip install -r requirements.txt
echo "[+] Installation complete! Run: python3 forgotten_core_v2.py"
