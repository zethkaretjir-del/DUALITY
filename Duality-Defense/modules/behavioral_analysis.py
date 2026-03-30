#!/usr/bin/env python3
# BEHAVIORAL ANALYSIS - Deteksi anomali sistem
import os
import json
import time
import psutil
from datetime import datetime

class BehavioralAnalysis:
    def __init__(self):
        self.baseline_file = os.path.expanduser("~/.awakened_core/behavior_baseline.json")
        self.anomaly_log = os.path.expanduser("~/.awakened_core/anomalies.log")
        self.baseline = self.load_baseline()
    
    def load_baseline(self):
        if os.path.exists(self.baseline_file):
            with open(self.baseline_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_baseline(self):
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
    
    def learn(self, days=7):
        """Learn normal behavior"""
        print(f"[*] Learning mode for {days} days...")
        data = []
        
        for day in range(days):
            day_data = {
                "date": str(datetime.now()),
                "cpu_avg": [],
                "memory_avg": [],
                "connections_avg": []
            }
            
            for hour in range(24):
                cpu = psutil.cpu_percent(interval=60)
                mem = psutil.virtual_memory().percent
                conn = len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
                
                day_data["cpu_avg"].append(cpu)
                day_data["memory_avg"].append(mem)
                day_data["connections_avg"].append(conn)
                
                print(f"  Day {day+1}/{days}, Hour {hour+1}/24: CPU={cpu}%, MEM={mem}%")
            
            data.append(day_data)
        
        self.baseline = {
            "cpu_normal": sum([sum(d["cpu_avg"])/len(d["cpu_avg"]) for d in data])/len(data),
            "cpu_std": 10,
            "memory_normal": sum([sum(d["memory_avg"])/len(d["memory_avg"]) for d in data])/len(data),
            "memory_std": 10,
            "connections_normal": sum([sum(d["connections_avg"])/len(d["connections_avg"]) for d in data])/len(data),
            "connections_std": 5
        }
        
        self.save_baseline()
        print("[+] Baseline saved!")
    
    def detect_anomalies(self):
        """Deteksi anomali real-time"""
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        conn = len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
        
        anomalies = []
        
        if cpu > self.baseline.get("cpu_normal", 50) + self.baseline.get("cpu_std", 10):
            anomalies.append(f"High CPU: {cpu}% (normal: {self.baseline.get('cpu_normal', 50)}%)")
        
        if mem > self.baseline.get("memory_normal", 50) + self.baseline.get("memory_std", 10):
            anomalies.append(f"High Memory: {mem}% (normal: {self.baseline.get('memory_normal', 50)}%)")
        
        if conn > self.baseline.get("connections_normal", 10) + self.baseline.get("connections_std", 5):
            anomalies.append(f"High Connections: {conn} (normal: {self.baseline.get('connections_normal', 10)})")
        
        if anomalies:
            with open(self.anomaly_log, 'a') as f:
                f.write(f"{datetime.now()}: {anomalies}\n")
            return anomalies
        return []

if __name__ == "__main__":
    ba = BehavioralAnalysis()
    ba.learn(1)  # Test 1 hari
    print(ba.detect_anomalies())
