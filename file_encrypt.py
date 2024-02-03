from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

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

def encrypt_file(file_path, password):
    salt = b'yourAppName'
    key = generate_key_from_password(password, salt)
    cipher = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = cipher.encrypt(original)

    with open('demo_something.txt', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Example usage
file_path = 'demo.txt'
password = 'test'
encrypt_file(file_path, password)

#install 
    
    #pip install cryptography
    #pip install hashlib