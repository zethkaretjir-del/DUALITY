#!/bin/bash
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              FORGOTTEN CORE INSTALLER                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"

# Install dependencies
if command -v pkg &> /dev/null; then
    echo "[*] Installing for Termux..."
    pkg update -y
    pkg install -y python python-pip tor
    pip install requests
else
    echo "[*] Installing for Kali Linux..."
    apt update -y
    apt install -y python3 python3-pip tor
    pip3 install requests
fi

# Create directories
mkdir -p ~/.forgotten_core/shadow_payloads

# Copy main file
if [ -d "/data/data/com.termux" ]; then
    cp forgotten_core.py /data/data/com.termux/files/usr/bin/forgotten_core
    chmod +x /data/data/com.termux/files/usr/bin/forgotten_core
    echo "[+] Installed to Termux"
else
    cp forgotten_core.py /usr/local/bin/forgotten_core
    chmod +x /usr/local/bin/forgotten_core
    echo "[+] Installed to Kali Linux"
fi

echo ""
echo -e "\033[92m[+] Forgotten Core installed successfully!\033[0m"
echo -e "    Run: forgotten_core"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Copyright © RianModss - Architect 02"
echo "═══════════════════════════════════════════════════════════════"
