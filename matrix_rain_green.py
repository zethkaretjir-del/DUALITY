#!/usr/bin/env python3
import os
import sys
import time
import random

def matrix_rain(duration=8, fall_speed=1.5):
    """Animasi Matrix rain - warna hijau khas Matrix"""
    os.system('clear')
    
    # Ukuran terminal
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    
    chars = "01"
    
    # Warna hijau khas Matrix
    GREEN_BRIGHT = '\033[92m'   # Hijau terang (kepala)
    GREEN_DARK = '\033[32m'      # Hijau gelap (ekor)
    
    # Posisi setiap kolom
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.3, 0.6) * fall_speed,
            'length': random.randint(5, 15)
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
                    data['speed'] = random.uniform(0.3, 0.6) * fall_speed
                    data['length'] = random.randint(5, 15)
                
                # Gambar trail
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        if i == 0:
                            frame[y][x] = f"{GREEN_BRIGHT}{random.choice(chars)}\033[0m"
                        else:
                            frame[y][x] = f"{GREEN_DARK}{random.choice(chars)}\033[0m"
            
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
    
    print("\n" * rows)
    os.system('clear')
    print(f"\033[92m✨ Matrix rain selesai! ✨\033[0m")

if __name__ == "__main__":
    time.sleep(1)
    matrix_rain(duration=8, fall_speed=1.5)

