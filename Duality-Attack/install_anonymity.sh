#!/bin/bash
# install_anonymity.sh - Void Anonymity Module Installer

echo "[*] Installing Void Anonymity Module..."

# Install anonymity tools
if command -v pkg &> /dev/null; then
    pkg install -y tor proxychains-ng macchanger
else
    apt install -y tor proxychains-ng macchanger
fi

# Install Python dependencies
pip3 install requests[socks] pysocks stem
pip3 install pycryptodome dnspython

# Download proxy lists
mkdir -p ~/.forgotten_core/proxies
curl -s "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all" > ~/.forgotten_core/proxies/socks5.txt
curl -s "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt" >> ~/.forgotten_core/proxies/socks5.txt

echo "[+] Void Anonymity Module installed!"
