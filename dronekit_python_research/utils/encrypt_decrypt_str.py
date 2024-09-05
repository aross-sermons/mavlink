from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

KEY_SIZE = 32 # 256 bits
IV_SIZE = 16 # 128 bits
KEY_FILE = 'aes_key.txt'

def str_to_file(filename: str, data: str):
    """
    Writes a string to a .txt file.

    :param filename: The name of the file to write to.
    :param data: The data to be written.
    """
    with open(filename, 'w') as file:
        file.write(data)

def str_from_file(filename: str) -> str:
    """
    Reads a string from a .txt file.

    :param filename: The name of the file to read from.
    :return: The string in the file.
    """
    with open(filename, 'r') as file:
        return file.read()

def generate_aes_key() -> str:
    """
    
    """
    return base64.b64encode(urandom(KEY_SIZE)).decode('utf-8')

def encrypt_str(plaintext: str, key: str) -> str:
    """
    
    """
    key = base64.b64decode(key)
    iv = urandom(IV_SIZE)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_str(encrypted_str: str, key: str) -> str:
    """
    
    """
    key = base64.b64decode(key)
    encrypted_data = base64.b64decode(encrypted_str)

    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')