#!/bin/bash
# DUALITY Attack Framework Installer

echo -e "\033[91m"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              DUALITY ATTACK FRAMEWORK INSTALLER               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Installing..."
    if command -v pkg &> /dev/null; then
        pkg install python3 -y
    else
        sudo apt install python3 python3-pip -y
    fi
fi

# Install dependencies
echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

# Create executable
chmod +x duality.py

# Create symlink (optional)
if [ -d "/data/data/com.termux" ]; then
    cp duality.py /data/data/com.termux/files/usr/bin/duality
    chmod +x /data/data/com.termux/files/usr/bin/duality
    echo "[+] Installed to Termux"
else
    sudo cp duality.py /usr/local/bin/duality
    sudo chmod +x /usr/local/bin/duality
    echo "[+] Installed to /usr/local/bin"
fi

echo ""
echo -e "\033[92m[+] DUALITY Attack Framework installed successfully!\033[0m"
echo -e "\033[96m[*] Run: python3 duality.py\033[0m"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Copyright © RianModss - Architect 02"
echo "═══════════════════════════════════════════════════════════════"
