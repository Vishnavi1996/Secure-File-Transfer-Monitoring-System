import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_or_generate_key():
    """Loads the encryption key or generates one if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

_key = load_or_generate_key()
_cipher = Fernet(_key)

def encrypt(data: str) -> str:
    """Encrypts a string."""
    return _cipher.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt(data: str) -> str:
    """Decrypts a string."""
    try:
        return _cipher.decrypt(data.encode('utf-8')).decode('utf-8')
    except Exception:
        return "<Decryption Failed>"
