#!/usr/bin/env python3
import os
import sys
import time
import random

def matrix_rain_cyan(duration=8, fall_speed=1.5):
    """
    Animasi Matrix rain - warna cyan
    """
    os.system('clear')
    
    # Ukuran terminal
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    
    # Karakter beragam
    chars = "ktoncTTXCL5@#CNQrmsbUVrpf aM(w eouk%GehF iJijl.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    
    # Warna cyan
    CYAN_BRIGHT = '\033[96m'    # Cyan terang (kepala)
    CYAN_MEDIUM = '\033[36m'    # Cyan sedang
    CYAN_DARK = '\033[38;5;30m' # Cyan gelap (ekor)
    WHITE = '\033[97m'          # Putih (aksen)
    BLACK = '\033[30m'          # Hitam (background)
    
    # Background hitam
    print('\033[40m', end='')
    
    # Posisi setiap kolom
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.2, 0.5) * fall_speed,
            'length': random.randint(5, 15),
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
                
                # Gambar trail dengan warna cyan
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        char = random.choice(chars)
                        if i == 0:
                            # Kepala: Cyan terang
                            frame[y][x] = f"{CYAN_BRIGHT}{char}\033[0m\033[40m"
                        elif i == 1:
                            # Kedua: Putih (opsional, biar keliatan keren)
                            frame[y][x] = f"{WHITE}{char}\033[0m\033[40m"
                        elif i == 2:
                            # Ketiga: Cyan sedang
                            frame[y][x] = f"{CYAN_MEDIUM}{char}\033[0m\033[40m"
                        else:
                            # Ekor: Cyan gelap
                            if random.choice([True, False]):
                                frame[y][x] = f"{CYAN_DARK}{char}\033[0m\033[40m"
                            else:
                                frame[y][x] = f"{BLACK}{char}\033[0m\033[40m"
            
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

if __name__ == "__main__":
    time.sleep(1)
    matrix_rain_cyan(duration=8, fall_speed=1.5)
