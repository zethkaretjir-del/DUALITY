#!/usr/bin/env python3
import os
import sys
import time
import random

def matrix_rain_styled(duration=8, fall_speed=1.5):
    """
    Animasi Matrix rain dengan karakter berantakan
    Kayak font stylized/random character
    """
    os.system('clear')
    
    # Ukuran terminal
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    
    # Karakter random yang lebih variatif (kayak di screenshot)
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~ktoncTTXCL5@#CNQrmsbUVrpf aM(w eouk%GehF iJijl."
    
    # Warna hijau khas Matrix
    GREEN_BRIGHT = '\033[92m'
    GREEN_DARK = '\033[32m'
    
    # Background hitam
    print('\033[40m', end='')
    
    # Posisi setiap kolom
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.2, 0.5) * fall_speed,
            'length': random.randint(5, 15),
            'chars': [random.choice(chars) for _ in range(rows)]  # random char per baris
        })
    
    end_time = time.time() + duration
    
    try:
        while time.time() < end_time:
            # Buat frame
            frame = [[' ' for _ in range(columns)] for _ in range(rows)]
            
            # Update setiap kolom
            for x in range(columns):
                data = columns_data[x]
                data['y'] += data['speed']
                
                if data['y'] > rows + data['length']:
                    data['y'] = -data['length']
                    data['speed'] = random.uniform(0.2, 0.5) * fall_speed
                    data['length'] = random.randint(5, 15)
                    # Ganti karakter di kolom ini
                    data['chars'] = [random.choice(chars) for _ in range(rows)]
                
                # Gambar trail
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        # Pake karakter random dari kolom
                        char = data['chars'][y % len(data['chars'])]
                        if i == 0:
                            frame[y][x] = f"{GREEN_BRIGHT}{char}\033[0m\033[40m"
                        else:
                            # Semakin ke bawah semakin gelap
                            brightness = 90 - (i * 5)
                            if brightness < 30:
                                brightness = 30
                            frame[y][x] = f"\033[38;5;{brightness}m{char}\033[0m\033[40m"
            
            # Render frame
            output = []
            for y in range(rows):
                output.append(''.join(frame[y]))
            
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(output))
            sys.stdout.flush()
            
            time.sleep(0.03)
    
    except KeyboardInterrupt:
        pass
    
    print("\033[0m" * rows)
    os.system('clear')
    print(f"\033[92m✨ Matrix rain selesai! ✨\033[0m")

if __name__ == "__main__":
    print(f"\033[92m[*] Memulai animasi Matrix rain stylized...\033[0m")
    print(f"\033[92m[*] Durasi: 8 detik\033[0m")
    print(f"\033[92m[*] Karakter beragam: huruf, angka, simbol\033[0m")
    time.sleep(1)
    matrix_rain_styled(duration=8, fall_speed=1.5)
