#!/usr/bin/env python3
# ALERT MANAGER - Kirim notifikasi ke Telegram/Discord
import requests
import json
import os
from datetime import datetime

class AlertManager:
    def __init__(self):
        self.telegram_token = None
        self.telegram_chat_id = None
        self.discord_webhook = None
        self.load_config()
    
    def load_config(self):
        config_file = os.path.expanduser("~/.awakened_core/alert_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.telegram_token = config.get('telegram_token')
                self.telegram_chat_id = config.get('telegram_chat_id')
                self.discord_webhook = config.get('discord_webhook')
    
    def send_telegram(self, message):
        """Kirim alert ke Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            return False
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message}
            requests.post(url, json=data, timeout=5)
            return True
        except:
            return False
    
    def send_discord(self, message):
        """Kirim alert ke Discord"""
        if not self.discord_webhook:
            return False
        try:
            data = {"content": message}
            requests.post(self.discord_webhook, json=data, timeout=5)
            return True
        except:
            return False
    
    def send_alert(self, title, message, level="INFO"):
        """Kirim alert ke semua channel"""
        alert_msg = f"[{level}] {title}\n{message}\nTime: {datetime.now()}"
        self.send_telegram(alert_msg)
        self.send_discord(alert_msg)
        
        # Log ke file
        log_file = os.path.expanduser("~/.awakened_core/alerts.log")
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now()}: {alert_msg}\n")
    
    def configure(self):
        """Konfigurasi alert"""
        print("\n[*] Alert Configuration")
        self.telegram_token = input("Telegram Bot Token (kosongkan jika tidak): ") or None
        self.telegram_chat_id = input("Telegram Chat ID: ") or None
        self.discord_webhook = input("Discord Webhook URL: ") or None
        
        config = {
            "telegram_token": self.telegram_token,
            "telegram_chat_id": self.telegram_chat_id,
            "discord_webhook": self.discord_webhook
        }
        
        os.makedirs(os.path.expanduser("~/.awakened_core"), exist_ok=True)
        with open(os.path.expanduser("~/.awakened_core/alert_config.json"), 'w') as f:
            json.dump(config, f)
        
        print("[+] Alert configured!")

if __name__ == "__main__":
    alert = AlertManager()
    alert.configure()
    alert.send_alert("Test", "Alert system working!", "INFO")
