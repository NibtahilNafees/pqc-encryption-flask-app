from cryptography.fernet import Fernet

def generate_keypair():
    """Generate a symmetric key for Fernet."""
    key = Fernet.generate_key()
    return key, key  # Using same key for encrypt/decrypt for demo

def encrypt_message(message: bytes, key: bytes) -> bytes:
    """Encrypt a message using Fernet."""
    f = Fernet(key)
    return f.encrypt(message)

def decrypt_message(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt a message using Fernet."""
    f = Fernet(key)
    return f.decrypt(ciphertext)
