from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:

    def __init__(self):
        self.BLOCK_SIZE = 16

    def pad(self, data):
        return data + (self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)

    def unpad(self, data):
        return data[:-ord(data[len(data) - 1:])]

    def encrypt(self, data, key):
        data = self.pad(data).encode()
        f = Fernet(key)
        return f.encrypt(data).decode()

    def decrypt(self, data, key):
        f = Fernet(key)
        return self.unpad(f.decrypt(data).decode())

    def get_key(self, password_provided):
        password = password_provided.encode()
        salt = b'g\x9dF\xfa?Ix`64\xb3*K~S#'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))
