
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Security:
    def __init__(self):
        self.key = None
        self.load_key()
        
    def load_key(self):
        try:
            with open("key.bin", "rb") as key_file:
                self.key = key_file.read()
        except:
            self.key = Fernet.generate_key()
            with open("key.bin", "wb") as key_file:
                key_file.write(self.key)
                
    def encrypt_data(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        return f.decrypt(encrypted_data).decode()
