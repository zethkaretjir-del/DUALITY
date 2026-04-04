#!/usr/bin/env python3
from core.colors import Colors

class ROT13Tool:
    def __init__(self):
        self.name = "ROT13 Cipher"
    
    def rot13(self, text):
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)
    
    def run(self):
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        text = input(f"{Colors.GREEN}Text > {Colors.END}")
        print(f"{Colors.GREEN}[+] Result: {self.rot13(text)}{Colors.END}")

if __name__ == "__main__":
    tool = ROT13Tool()
    tool.run()
