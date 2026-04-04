#!/usr/bin/env python3
# AI ASSISTANT - Chatbot buat DUALITY
# "Tanya apa aja tentang DUALITY"
import os
import random
import time
from core.colors import Colors

class AIAssistant:
    def __init__(self):
        self.name = "AI Assistant"
        self.responses = {
            "hello": ["Halo! Ada yang bisa dibantu?", "Hi! Butuh bantuan?", "Hai! Mau nanya apa?"],
            "help": ["Coba ketik 'help' di menu utama", "Perintah: phone, ip, payload, dll", "Bantuan lengkap: https://github.com/zethkaretjir-del/Duality"],
            "phone": ["Phone tracker: lacak info nomor HP", "Contoh: phone +628123456789", "Dapetin provider, lokasi, link WhatsApp"],
            "ip": ["IP tracker: lacak lokasi IP", "Contoh: ip 8.8.8.8", "Dapetin negara, kota, ISP"],
            "payload": ["Payload generator: bikin reverse shell", "Contoh: payload lalu masukkan LHOST dan LPORT", "Support Python, Bash, PHP, PowerShell"],
            "ddos": ["DDoS module: stress test server", "Gunakan dengan bijak! Hanya untuk testing", "Bisa HTTP flood, SYN flood, UDP flood"],
            "spam": ["Email spammer: kirim email massal", "Butuh App Password Gmail", "Bisa kirim 100+ email sekaligus"],
            "wifi": ["WiFi cracker: crack password WiFi", "Butuh aircrack-ng dan adapter khusus", "Bisa capture handshake dan crack"],
            "cam": ["Camera hack: scan IP camera", "Cari kamera tanpa password", "Contoh: camhack lalu pilih scan"],
            "pentest": ["Auto pentest report: generate laporan", "Scan subdomain, port, teknologi", "Hasil dalam format HTML"],
            "phish": ["Phishing generator: buat halaman palsu", "Support Facebook, Google, Instagram", "Jalankan dengan php -S 0.0.0.0:8080"],
            "lanscan": ["LAN scanner: deteksi device di jaringan", "Lihat IP, MAC, vendor, hostname", "Bisa scan port juga"],
            "track": ["Phone tracker: lacak nomor HP", "Sama kayak 'phone' command", "Dapetin provider dan lokasi"],
            "encode": ["Encode/decode: base64, URL", "Contoh: encode lalu pilih base64", "Bisa encode teks atau file"],
            "crypt": ["File encryption: AES-256", "Enkripsi file penting", "Jangan lupa simpan key-nya"],
            "hash": ["Hash generator: MD5, SHA1, SHA256", "Buat hash dari teks", "Cocok buat password"],
            "passgen": ["Password generator: bikin password random", "Bisa atur panjang dan jumlah", "Hasil langsung di terminal"],
            "rot13": ["ROT13 cipher: encode/decode", "Pake pergeseran 13 huruf", "Contoh: rot13 Hello = Uryyb"],
            "find": ["Find wrapper: cari file", "Cari berdasarkan nama, ukuran, user", "Contoh: find -> pilih 1 -> *.py"],
            "botnet": ["Botnet C2 server: kontrol banyak device", "Jalankan server, generate client", "Kirim command massal"],
            "exploit": ["Auto exploiter: scan SQLi, XSS, LFI", "Contoh: exploit -> pilih target", "Dapetin potensi celah"],
            "steal": ["Password stealer: curi credential", "Ambil password Chrome, SSH keys", "Hasil disimpan ke file JSON"],
            "keylog": ["Keylogger: record keyboard", "Jalan di background", "Log disimpan di ~/.cache/.keylog"],
            "screenshot": ["Screenshot capture: ambil foto layar", "Butuh termux-api", "Hasil png di folder data"],
            "webcam": ["Webcam capture: ambil foto dari kamera", "Butuh termux-api", "Hasil jpg di folder data"],
            "update": ["Auto updater: update dari GitHub", "Cek update terbaru", "Pull perubahan otomatis"],
        }
        
        self.fallback = [
            "Maaf, aku belum paham. Coba ketik 'help' buat liat command.",
            "Hmm, aku gak ngerti. Mungkin bisa tanya yang lain?",
            "Belum tau jawabannya. Coba tanya tentang command DUALITY aja.",
            "Wah, pertanyaan bagus! Tapi aku belum belajar itu. Coba 'help' ya."
        ]
    
    def get_response(self, query):
        query = query.lower().strip()
        
        # Cari keyword
        for keyword, responses in self.responses.items():
            if keyword in query:
                return random.choice(responses)
        
        # Cek command DUALITY
        duality_commands = [
            "phone", "ip", "username", "subdomain", "port", "dork", "email", 
            "whois", "dns", "payload", "ddos", "stealth", "anon", "c2", 
            "track", "spam", "crypt", "hash", "encode", "passgen", "malware",
            "rot13", "find", "botnet", "ai", "exploit", "persist", "transfer",
            "screenshot", "keylog", "steal", "miner", "update", "darkweb",
            "webcam", "subenum", "emailscrape", "linkextract", "dirbrute",
            "portadv", "phish", "wificrack", "camhack", "pentest", "ddospanel",
            "exploitdb", "lanscan"
        ]
        
        for cmd in duality_commands:
            if cmd in query:
                return f"Command '{cmd}' ada di DUALITY. Ketik '{cmd}' buat jalanin. Mau penjelasan? Ketik 'help {cmd}'"
        
        # Fallback
        return random.choice(self.fallback)
    
    def run(self):
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       🤖 AI ASSISTANT - DUALITY HELP{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.DIM}Type 'exit' to quit, 'help' for available topics{Colors.END}\n")
        
        print(f"{Colors.GREEN}[+] AI Assistant ready!{Colors.END}")
        print(f"{Colors.YELLOW}[!] Tanya tentang command DUALITY atau fitur tertentu{Colors.END}\n")
        
        while True:
            try:
                query = input(f"{Colors.RED}┌──({Colors.GREEN}ai{Colors.RED}@{Colors.CYAN}duality{Colors.RED})-{Colors.BLUE}[~]{Colors.RED}\n└─{Colors.WHITE}$ {Colors.END}")
                
                if query.lower() in ['exit', 'quit', 'q']:
                    print(f"{Colors.GREEN}[+] AI Assistant exited{Colors.END}")
                    break
                
                if query.lower() == 'help':
                    print(f"\n{Colors.CYAN}Available topics:{Colors.END}")
                    topics = list(self.responses.keys())[:10]
                    for t in topics:
                        print(f"  {Colors.GREEN}• {t}{Colors.END}")
                    print(f"  {Colors.DIM}... dan masih banyak lagi{Colors.END}\n")
                    continue
                
                response = self.get_response(query)
                print(f"{Colors.GREEN}[AI] {response}{Colors.END}\n")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}[+] AI Assistant exited{Colors.END}")
                break

if __name__ == "__main__":
    ai = AIAssistant()
    ai.run()
