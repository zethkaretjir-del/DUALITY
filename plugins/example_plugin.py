# Example Plugin untuk DUALITY
# Ini contoh plugin yang aman

def run(target="world"):
    """Fungsi utama yang akan dipanggil oleh plugin manager"""
    return f"Hello, {target}! Plugin berhasil dijalankan."

def get_info():
    return {
        "name": "Example Plugin",
        "version": "1.0",
        "author": "Rian",
        "description": "Contoh plugin sederhana untuk testing"
    }
