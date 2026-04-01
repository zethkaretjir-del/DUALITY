#!/usr/bin/env python3
# NETWORK SPEED TEST - Tes kecepatan internet

import os
import time
import threading
import requests
from core.colors import Colors

class SpeedTest:
    def __init__(self):
        self.name = "Network Speed Test"
        self.download_speed = 0
        self.upload_speed = 0
        self.ping = 0
    
    def test_ping(self):
        """Test ping ke Google DNS"""
        print(f"{Colors.CYAN}[*] Testing ping...{Colors.END}")
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '4', '8.8.8.8'], 
                                   capture_output=True, text=True, timeout=10)
            import re
            match = re.search(r'min/avg/max/(\d+\.\d+)', result.stdout)
            if match:
                self.ping = float(match.group(1))
            else:
                self.ping = 0
        except:
            self.ping = 0
    
    def test_download(self):
        """Test download speed"""
        print(f"{Colors.CYAN}[*] Testing download speed...{Colors.END}")
        try:
            # Download file test 10MB dari speedtest server
            url = "https://speedtest.tele2.net/10MB.zip"
            start_time = time.time()
            response = requests.get(url, stream=True, timeout=30)
            total_size = 0
            for chunk in response.iter_content(chunk_size=1024*1024):
                total_size += len(chunk)
                # Progress
                percent = (total_size / (10*1024*1024)) * 100
                print(f"\r{Colors.DIM}Downloading: {percent:.1f}%{Colors.END}", end="")
            end_time = time.time()
            duration = end_time - start_time
            size_mb = total_size / (1024 * 1024)
            self.download_speed = (size_mb * 8) / duration  # Mbps
            print()
        except Exception as e:
            print(f"{Colors.RED}[!] Download test failed: {e}{Colors.END}")
            self.download_speed = 0
    
    def test_upload(self):
        """Test upload speed (simulasi)"""
        print(f"{Colors.CYAN}[*] Testing upload speed...{Colors.END}")
        try:
            # Upload test dengan data dummy
            test_data = os.urandom(5 * 1024 * 1024)  # 5MB
            url = "https://httpbin.org/post"
            start_time = time.time()
            response = requests.post(url, data=test_data, timeout=30)
            end_time = time.time()
            duration = end_time - start_time
            size_mb = 5  # 5MB
            self.upload_speed = (size_mb * 8) / duration  # Mbps
        except Exception as e:
            print(f"{Colors.RED}[!] Upload test failed: {e}{Colors.END}")
            self.upload_speed = 0
    
    def run_speedtest(self):
        """Run all speed tests"""
        print(f"\n{Colors.CYAN}[*] Starting network speed test...{Colors.END}\n")
        
        # Test ping
        self.test_ping()
        
        # Test download
        self.test_download()
        
        # Test upload
        self.test_upload()
        
        # Display results
        print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📊 SPEED TEST RESULTS{Colors.END}")
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
        
        # Ping
        if self.ping > 0:
            ping_color = Colors.GREEN if self.ping < 50 else Colors.YELLOW if self.ping < 100 else Colors.RED
            print(f"{Colors.WHITE}  {Colors.CYAN}Ping:{Colors.END} {ping_color}{self.ping:.1f} ms{Colors.END}")
        else:
            print(f"{Colors.WHITE}  {Colors.CYAN}Ping:{Colors.END} {Colors.RED}Failed{Colors.END}")
        
        # Download
        if self.download_speed > 0:
            speed_color = Colors.GREEN if self.download_speed > 10 else Colors.YELLOW if self.download_speed > 5 else Colors.RED
            print(f"{Colors.WHITE}  {Colors.CYAN}Download:{Colors.END} {speed_color}{self.download_speed:.2f} Mbps{Colors.END}")
        else:
            print(f"{Colors.WHITE}  {Colors.CYAN}Download:{Colors.END} {Colors.RED}Failed{Colors.END}")
        
        # Upload
        if self.upload_speed > 0:
            speed_color = Colors.GREEN if self.upload_speed > 5 else Colors.YELLOW if self.upload_speed > 2 else Colors.RED
            print(f"{Colors.WHITE}  {Colors.CYAN}Upload:{Colors.END} {speed_color}{self.upload_speed:.2f} Mbps{Colors.END}")
        else:
            print(f"{Colors.WHITE}  {Colors.CYAN}Upload:{Colors.END} {Colors.RED}Failed{Colors.END}")
        
        print(f"{Colors.GREEN}{'='*55}{Colors.END}")
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.YELLOW}[!] This test will use ~15MB of data{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Run Speed Test")
        print(f"{Colors.GREEN}[2]{Colors.END} Quick Ping Only")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.run_speedtest()
        elif choice == '2':
            self.test_ping()
            print(f"\n{Colors.GREEN}Ping: {self.ping:.1f} ms{Colors.END}")

if __name__ == "__main__":
    test = SpeedTest()
    test.run()
