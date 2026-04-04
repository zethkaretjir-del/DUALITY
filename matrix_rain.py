#!/usr/bin/env python3
import os
import sys
import time
import random

def matrix_rain(duration=5, speed_multiplier=2.0):
    """Animasi Matrix rain - huruf jatuh ke bawah
       speed_multiplier: 1 = normal, 2 = 2x lipat, 3 = 3x lipat
    """
    os.system('clear')
    
    # Ukuran terminal
    try:
        import shutil
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24
    
    chars = "01"
    
    # Posisi setiap kolom
    columns_data = []
    for _ in range(columns):
        columns_data.append({
            'y': random.randint(-rows, 0),
            'speed': random.uniform(0.3, 0.8) * speed_multiplier,  # Lebih cepat
            'length': random.randint(5, 15)  # Trail lebih panjang
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
                    data['speed'] = random.uniform(0.3, 0.8) * speed_multiplier
                    data['length'] = random.randint(5, 15)
                
                # Gambar trail
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        if i == 0:
                            frame[y][x] = f"\033[92m{random.choice(chars)}\033[0m"
                        else:
                            brightness = 90 - (i * 5)
                            if brightness < 30:
                                brightness = 30
                            frame[y][x] = f"\033[38;5;{brightness}m{random.choice(chars)}\033[0m"
            
            # Render frame
            output = []
            for y in range(rows):
                output.append(''.join(frame[y]))
            
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(output))
            sys.stdout.flush()
            
            time.sleep(0.03)  # Refresh lebih cepat (dari 0.05 jadi 0.03)
    
    except KeyboardInterrupt:
        pass
    
    print("\n" * rows)
    os.system('clear')

if __name__ == "__main__":
    # Pilihan kecepatan
    print("Pilih kecepatan:")
    print("[1] Normal")
    print("[2] Cepat")
    print("[3] Sangat Cepat")
    print("[4] Kencang Banget")
    
    choice = input("\nPilih (1-4): ")
    
    speeds = {
        '1': 1.0,
        '2': 2.0,
        '3': 3.0,
        '4': 5.0
    }
    
    speed = speeds.get(choice, 2.0)
    matrix_rain(duration=5, speed_multiplier=speed)
