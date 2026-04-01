#!/usr/bin/env python3
# SPAM MODULE - Email & SMS Spammer
#!/usr/bin/env python3
# SPAM MODULE - Email & SMS Solution Provider
# "Flood the target or get the solution"

import os
import smtplib
import requests
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.colors import Colors
from core.utils import save_json, get_timestamp
from config.settings import DATA_DIR

class Spammer:
    """Email spammer and SMS solution provider"""
    
    def __init__(self):
        self.name = "Spammer Module"
        self.data_dir = f"{DATA_DIR}/spam"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def email_spam(self, sender_email, sender_password, target_email, subject, message, count, delay):
        """Send email spam"""
        success = 0
        failed = 0
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            
            for i in range(count):
                try:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = target_email
                    msg["Subject"] = f"{subject} [{i+1}]"
                    msg.attach(MIMEText(message, "plain"))
                    
                    server.send_message(msg)
                    success += 1
                    print(f"{Colors.GREEN}[✓] Email {i+1}/{count} terkirim{Colors.END}")
                    
                except Exception as e:
                    from core.utils import print_error
                    print_error(f"Spammer Failed: {e}")
                    return
                
                time.sleep(delay)
            
            server.quit()
            
        except Exception as e:
            print(f"{Colors.RED}[!] Connection error: {e}{Colors.END}")
        
        return success, failed
    
    def email_menu(self):
        """Email spam menu"""
        print(f"\n{Colors.YELLOW}[!] Gunakan akun email sendiri sebagai pengirim{Colors.END}")
        print(f"{Colors.YELLOW}[!] Gmail butuh App Password (bukan password asli){Colors.END}")
        
        sender_email = input(f"{Colors.WHITE}📧 Email pengirim: {Colors.END}")
        sender_password = input(f"{Colors.WHITE}🔑 App Password: {Colors.END}")
        target_email = input(f"{Colors.WHITE}🎯 Email target: {Colors.END}")
        subject = input(f"{Colors.WHITE}📝 Subject: {Colors.END}") or "Spam Message"
        message = input(f"{Colors.WHITE}💬 Pesan: {Colors.END}") or "You have been spammed!"
        
        try:
            count = int(input(f"{Colors.WHITE}🔢 Jumlah spam: {Colors.END}"))
        except:
            count = 10
        
        try:
            delay = float(input(f"{Colors.WHITE}⏱️ Delay (detik): {Colors.END}") or "1")
        except:
            delay = 1
        
        print(f"\n{Colors.CYAN}[*] Memulai spam ke {target_email}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Tekan Ctrl+C untuk berhenti{Colors.END}\n")
        
        try:
            success, failed = self.email_spam(sender_email, sender_password, target_email, subject, message, count, delay)
            print(f"\n{Colors.GREEN}[+] Selesai! Berhasil: {success}, Gagal: {failed}{Colors.END}")
            
            # Save log
            log = {
                "target": target_email,
                "success": success,
                "failed": failed,
                "count": count,
                "timestamp": get_timestamp()
            }
            filename = f"{self.data_dir}/spam_log_{int(time.time())}.json"
            save_json(log, filename)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Dihentikan oleh user{Colors.END}")
    
    # ==================== SMS SOLUTION MENU ====================
    
    def sms_solution_menu(self):
        """Menu untuk memberikan solusi SMS permanen"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.WHITE}       SMS SPAM - SOLUSI PERMANEN{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"""
{Colors.GREEN}[1]{Colors.END} 📜 Panduan & Integrasi API Berbayar
{Colors.GREEN}[2]{Colors.END} 💾 Generate Script Python (ASPSMS/Twilio)
{Colors.GREEN}[3]{Colors.END} 📱 Solusi Aplikasi Android Gratis
{Colors.GREEN}[4]{Colors.END} ⚠️ Informasi SMS Blaster (Fake BTS)
{Colors.GREEN}[0]{Colors.END} 🔙 Kembali
        """)
        
        choice = input(f"{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.show_paid_gateway_guide()
        elif choice == '2':
            self.generate_sms_script()
        elif choice == '3':
            self.show_android_apps_guide()
        elif choice == '4':
            self.show_sms_blaster_info()
    
    def show_paid_gateway_guide(self):
        """Menampilkan panduan API Gateway Berbayar"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}       📜 PANDUAN SMS GATEWAY BERBAYAR{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"""
{Colors.YELLOW}[1] ASPSMS (Rekomendasi untuk Indonesia){Colors.END}
{Colors.WHITE}   - Website: https://www.aspsms.com/id/{Colors.END}
{Colors.WHITE}   - Registrasi gratis, tanpa kartu kredit{Colors.END}
{Colors.WHITE}   - Dapatkan API Key dari dashboard{Colors.END}
{Colors.WHITE}   - Isi saldo minimal 10 Euro (~Rp170.000){Colors.END}
{Colors.WHITE}   - Harga per SMS ke Indonesia:{Colors.END}
{Colors.WHITE}     • Telkomsel: 1.75 Credit (~Rp1.200){Colors.END}
{Colors.WHITE}     • Indosat/XL: 2.75 Credit (~Rp1.900){Colors.END}
{Colors.WHITE}     • Tri: 3.75 Credit (~Rp2.600){Colors.END}

{Colors.YELLOW}[2] Twilio (Provider Global){Colors.END}
{Colors.WHITE}   - Website: https://www.twilio.com{Colors.END}
{Colors.WHITE}   - Daftar gratis, dapat kredit $15 untuk trial{Colors.END}
{Colors.WHITE}   - Harga SMS ke Indonesia: $0.14 (~Rp2.200){Colors.END}

{Colors.YELLOW}[3] SMS.to (Mudah untuk Pemula){Colors.END}
{Colors.WHITE}   - Website: https://sms.to{Colors.END}
{Colors.WHITE}   - Trial gratis tanpa kartu kredit{Colors.END}
{Colors.WHITE}   - Harga: $0.14 per SMS{Colors.END}
        """)
        
        input(f"\n{Colors.DIM}Press Enter untuk kembali...{Colors.END}")
    
    def generate_sms_script(self):
        """Generate file script Python untuk pengguna"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}       💾 GENERATE SCRIPT SMS GATEWAY{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}[1]{Colors.END} Script untuk ASPSMS")
        print(f"{Colors.GREEN}[2]{Colors.END} Script untuk Twilio")
        print(f"{Colors.GREEN}[3]{Colors.END} Script untuk SMS.to")
        
        choice = input(f"{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            filename = f"{self.data_dir}/aspsms_sender.py"
            script_content = '''#!/usr/bin/env python3
# ASPSMS SMS Gateway Script
# Daftar: https://www.aspsms.com/id/

import requests

# KONFIGURASI - GANTI DENGAN DATA ANDA
API_KEY = "ISI_API_KEY_ANDA"  # Dari dashboard ASPSMS
TARGET_NUMBER = "628123456789"  # Nomor target (format internasional)
MESSAGE = "Pesan dari DUALITY Framework!"

# JANGAN UBAH KODE DI BAWAH INI
def send_sms():
    url = "https://www.aspsms.com/asmx/send.asmx/SendSimple"
    params = {
        'UserKey': API_KEY,
        'Recipients': TARGET_NUMBER,
        'MessageText': MESSAGE
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"[+] Status: {response.text}")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    send_sms()
'''
        elif choice == '2':
            filename = f"{self.data_dir}/twilio_sender.py"
            script_content = '''#!/usr/bin/env python3
# Twilio SMS Gateway Script
# Daftar: https://www.twilio.com

from twilio.rest import Client

# KONFIGURASI - GANTI DENGAN DATA ANDA
ACCOUNT_SID = "ISI_ACCOUNT_SID_ANDA"
AUTH_TOKEN = "ISI_AUTH_TOKEN_ANDA"
FROM_NUMBER = "+1234567890"  # Nomor Twilio Anda
TARGET_NUMBER = "+628123456789"  # Nomor target
MESSAGE = "Pesan dari DUALITY Framework!"

# JANGAN UBAH KODE DI BAWAH INI
def send_sms():
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=MESSAGE,
            from_=FROM_NUMBER,
            to=TARGET_NUMBER
        )
        print(f"[+] SMS terkirim! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    send_sms()
'''
        elif choice == '3':
            filename = f"{self.data_dir}/smsto_sender.py"
            script_content = '''#!/usr/bin/env python3
# SMS.to SMS Gateway Script
# Daftar: https://sms.to

import requests

# KONFIGURASI - GANTI DENGAN DATA ANDA
API_KEY = "ISI_API_KEY_ANDA"  # Dari dashboard SMS.to
TARGET_NUMBER = "+628123456789"  # Nomor target
MESSAGE = "Pesan dari DUALITY Framework!"

# JANGAN UBAH KODE DI BAWAH INI
def send_sms():
    url = "https://api.sms.to/sms/send"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": MESSAGE,
        "to": TARGET_NUMBER
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            print(f"[+] SMS terkirim!")
            return True
        else:
            print(f"[-] Gagal: {response.text}")
            return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    send_sms()
'''
        else:
            print(f"{Colors.RED}[!] Pilihan tidak valid!{Colors.END}")
            return
        
        with open(filename, 'w') as f:
            f.write(script_content)
        
        print(f"\n{Colors.GREEN}[+] Script berhasil digenerate!{Colors.END}")
        print(f"{Colors.CYAN}[*] Lokasi: {filename}{Colors.END}")
        print(f"{Colors.YELLOW}[!] Edit file tersebut dan isi API Key Anda!{Colors.END}")
        
        input(f"\n{Colors.DIM}Press Enter untuk kembali...{Colors.END}")
    
    def show_android_apps_guide(self):
        """Menampilkan panduan aplikasi Android gratis"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}       📱 APLIKASI ANDROID GRATIS{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"""
{Colors.GREEN}[1] ReogDial{Colors.END}
{Colors.WHITE}   - Download: Google Play Store{Colors.END}
{Colors.WHITE}   - Registrasi dengan email{Colors.END}
{Colors.WHITE}   - Bisa kirim SMS gratis ke Indonesia{Colors.END}
{Colors.WHITE}   - Cara pakai:{Colors.END}
{Colors.WHITE}     1. Buka aplikasi ReogDial{Colors.END}
{Colors.WHITE}     2. Masukkan nomor tujuan{Colors.END}
{Colors.WHITE}     3. Ketik pesan{Colors.END}
{Colors.WHITE}     4. Tekan Kirim{Colors.END}

{Colors.GREEN}[2] ZMZ SMS{Colors.END}
{Colors.WHITE}   - Download: Google Play Store{Colors.END}
{Colors.WHITE}   - Aplikasi klasik untuk SMS gratis{Colors.END}
{Colors.WHITE}   - Masih berfungsi untuk beberapa operator{Colors.END}

{Colors.GREEN}[3] TextNow (Versi Mod){Colors.END}
{Colors.WHITE}   - Dapat nomor virtual gratis{Colors.END}
{Colors.WHITE}   - Bisa kirim SMS ke internasional{Colors.END}
        """)
        
        input(f"\n{Colors.DIM}Press Enter untuk kembali...{Colors.END}")
    
    def show_sms_blaster_info(self):
        """Informasi teknis SMS Blaster (Ekstrim)"""
        print(f"\n{Colors.RED}{Colors.BOLD}{'═'*55}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}       ⚠️ INFORMASI SMS BLASTER (FAKE BTS){Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'═'*55}{Colors.END}")
        
        print(f"""
{Colors.RED}[!] PERINGATAN! Metode ini ILEGAL dan BERISIKO tinggi!{Colors.END}
{Colors.RED}[!] Hanya untuk PENGETAHUAN TEKNIS semata!{Colors.END}
{Colors.RED}[!] Penggunaan untuk spam dapat dikenakan sanksi hukum!{Colors.END}

{Colors.CYAN}📡 Prinsip Kerja:{Colors.END}
{Colors.WHITE}   - Memanfaatkan kelemahan protokol 2G (GSM){Colors.END}
{Colors.WHITE}   - Membuat BTS (Base Transceiver Station) palsu{Colors.END}
{Colors.WHITE}   - Menangkap dan mengirim SMS tanpa biaya{Colors.END}
{Colors.WHITE}   - Bisa spoofing nomor pengirim{Colors.END}

{Colors.CYAN}💻 Perangkat Keras yang Dibutuhkan:{Colors.END}
{Colors.WHITE}   - Software Defined Radio (SDR){Colors.END}
{Colors.WHITE}     • BladeRF (harga ~$500){Colors.END}
{Colors.WHITE}     • USRP (harga ~$1000+) {Colors.END}
{Colors.WHITE}     • HackRF One (harga ~$300){Colors.END}
{Colors.WHITE}   - PC/Laptop dengan performa tinggi{Colors.END}
{Colors.WHITE}   - Antenna yang sesuai frekuensi GSM{Colors.END}
{Colors.WHITE}   - SIM card (untuk testing){Colors.END}

{Colors.CYAN}📦 Software Pendukung:{Colors.END}
{Colors.WHITE}   - OpenBTS (open source){Colors.END}
{Colors.WHITE}   - YateBTS (komersial){Colors.END}
{Colors.WHITE}   - OsmocomBB (untuk penelitian){Colors.END}
{Colors.WHITE}   - gr-gsm (GNU Radio block untuk GSM){Colors.END}

{Colors.CYAN}🔧 Langkah Sederhana (Konsep):{Colors.END}
{Colors.WHITE}   1. Install SDR dan driver{Colors.END}
{Colors.WHITE}   2. Scan frekuensi GSM di area{Colors.END}
{Colors.WHITE}   3. Konfigurasi OpenBTS{Colors.END}
{Colors.WHITE}   4. Setel agar perangkat terhubung ke BTS palsu{Colors.END}
{Colors.WHITE}   5. Kirim SMS melalui antarmuka OpenBTS{Colors.END}

{Colors.RED}[!] Metode ini TIDAK DIREKOMENDASIKAN untuk spam!{Colors.END}
{Colors.RED}[!] Gunakan hanya untuk RISET dan PEMBELAJARAN!{Colors.END}
        """)
        
        input(f"\n{Colors.DIM}Press Enter untuk kembali...{Colors.END}")
    
    # ==================== MAIN MENU ====================
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} 📧 Email Spammer (SMTP) - WORKING")
        print(f"{Colors.GREEN}[2]{Colors.END} 📱 SMS Solution - Permanen")
        print(f"{Colors.GREEN}[0]{Colors.END} 🔙 Back")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.email_menu()
        elif choice == '2':
            self.sms_solution_menu()
        elif choice == '0':
            return
        else:
            print(f"{Colors.RED}[!] Pilihan tidak valid!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    spammer = Spammer()
    spammer.run()
