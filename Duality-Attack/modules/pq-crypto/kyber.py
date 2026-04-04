#!/usr/bin/env python3
# Post-Quantum Cryptography - Kyber (Lattice-based)
# Implementasi sederhana untuk edukasi

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class KyberPQC:
    """
    Simulasi Kyber Key Encapsulation Mechanism (KEM)
    Ini adalah VERSI EDUKASI (bukan implementasi nyata untuk produksi)
    """
    
    def __init__(self):
        self.name = "Kyber-512 (Lattice-based KEM)"
        self.key_size = 32  # 256-bit AES key
    
    def generate_keypair(self):
        """Generate keypair (simulasi)"""
        # Seed dari random ditambah timestamp
        seed = os.urandom(32)
        
        # Public key (simulasi)
        public_key = hashlib.sha256(seed + b"pub").digest()
        
        # Secret key (simulasi)
        secret_key = hashlib.sha256(seed + b"sec").digest()
        
        return public_key, secret_key
    
    def encapsulate(self, public_key):
        """Enkapsulasi shared secret"""
        # Simulasi shared secret
        shared_secret = os.urandom(self.key_size)
        
        # Ciphertext (simulasi)
        ciphertext = hashlib.sha256(public_key + shared_secret).digest()
        
        return shared_secret, ciphertext
    
    def decapsulate(self, secret_key, ciphertext):
        """Dekapsulasi shared secret"""
        # Simulasi decapsulate
        shared_secret = hashlib.sha256(secret_key + ciphertext).digest()[:self.key_size]
        return shared_secret
    
    def encrypt_aes(self, plaintext, key):
        """AES-GCM encryption with quantum-resistant key"""
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext
    
    def decrypt_aes(self, encrypted_data, key):
        """AES-GCM decryption"""
        iv = encrypted_data[:12]
        tag = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()
    
    def run_demo(self):
        """Demo mode"""
        print("\n🔐 POST-QUANTUM CRYPTO DEMO (Kyber)")
        print("="*50)
        
        # Alice buat keypair
        alice_pub, alice_sec = self.generate_keypair()
        print(f"Alice Public Key: {alice_pub.hex()[:32]}...")
        print(f"Alice Secret Key: {alice_sec.hex()[:32]}...")
        
        # Bob encapsulate
        shared_secret, ciphertext = self.encapsulate(alice_pub)
        print(f"\nBob Shared Secret: {shared_secret.hex()[:32]}...")
        
        # Alice decapsulate
        decrypted_secret = self.decapsulate(alice_sec, ciphertext)
        print(f"Alice Decrypted: {decrypted_secret.hex()[:32]}...")
        
        if shared_secret == decrypted_secret:
            print("\n✅ Shared secret match! Quantum-resistant encryption works!")
        else:
            print("\n❌ Shared secret mismatch!")
        
        # Test encrypt dengan AES
        plaintext = "This is a secret message that will survive quantum computers!"
        print(f"\n📝 Plaintext: {plaintext}")
        
        encrypted = self.encrypt_aes(plaintext, shared_secret)
        print(f"🔒 Encrypted: {encrypted.hex()[:64]}...")
        
        decrypted = self.decrypt_aes(encrypted, decrypted_secret)
        print(f"🔓 Decrypted: {decrypted}")
        
        return shared_secret == decrypted_secret

if __name__ == "__main__":
    kyber = KyberPQC()
    kyber.run_demo()
