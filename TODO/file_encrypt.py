from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

def generate_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=10000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_file(original, password):
    salt = b'todo'
    key = generate_key_from_password(password, salt)
    
    # Encode the key to make it suitable for Fernet
    encoded_key = base64.urlsafe_b64encode(key)
    
    cipher = Fernet(encoded_key)

    encrypted_data = cipher.encrypt(original)
    return encrypted_data

def decrypt_file(encrypted, password):
    salt = b'todo'
    key = generate_key_from_password(password, salt)
    
    # Encode the key to make it suitable for Fernet
    encoded_key = base64.urlsafe_b64encode(key)
    
    cipher = Fernet(encoded_key)

    decrypted_data = cipher.decrypt(encrypted)
    return decrypted_data
