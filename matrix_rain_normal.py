#!/usr/bin/env python3
import os
import sys
import time
import random

def matrix_rain(duration=8, speed_multiplier=1.0):
    """Animasi Matrix rain - huruf jatuh ke bawah
       duration: 8 detik
       speed_multiplier: 1.0 = normal
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
            'speed': random.uniform(0.1, 0.3) * speed_multiplier,
            'length': random.randint(3, 10)
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
                    data['speed'] = random.uniform(0.1, 0.3) * speed_multiplier
                    data['length'] = random.randint(3, 10)
                
                # Gambar trail
                for i in range(data['length']):
                    y = int(data['y'] - i)
                    if 0 <= y < rows:
                        if i == 0:
                            frame[y][x] = f"\033[92m{random.choice(chars)}\033[0m"
                        else:
                            frame[y][x] = f"\033[32m{random.choice(chars)}\033[0m"
            
            # Render frame
            output = []
            for y in range(rows):
                output.append(''.join(frame[y]))
            
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(output))
            sys.stdout.flush()
            
            time.sleep(0.05)  # Refresh normal
    
    except KeyboardInterrupt:
        pass
    
    print("\n" * rows)
    os.system('clear')
    print(f"{Colors.GREEN}{Colors.BOLD}✨ Matrix rain selesai! ✨{Colors.END}")

if __name__ == "__main__":
    print(f"{Colors.CYAN}[*] Memulai animasi Matrix rain...{Colors.END}")
    print(f"{Colors.CYAN}[*] Durasi: 8 detik{Colors.END}")
    time.sleep(1)
    matrix_rain(duration=8, speed_multiplier=1.0)
