import json
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from os import urandom

def generate_key() -> bytes:
    """
    Returns a key of fixed size 32 bytes.

    :return: The key
    """
    return urandom(32)

def encrypt_data(data:bytes, key:bytes):
    """
    Encrypts the given data with the given key. Returns a nonce and encrypted bytes.

    :param data: The data to be encrypted.
    :param key: The key to encrypt with.
    """
    # Validate parameters.
    if data == None or key == None:
        raise ValueError("data and key cannot be None")
    if type(data) == str:
        data = data.encode('utf-8')
    if type(data) != bytes:
        raise ValueError("data must be of type bytes")
    
    # Create cipher and encrypt data.
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data)

    # Return the nonce and encrypted data.
    return cipher.nonce, ciphertext

def decrypt_data(nonce:bytes, encrypted_data:bytes, key:bytes):
    """
    Decrypts the given data with the given key and nonce. Returns a string.

    :param encrypted_data: The encrypted data in bytes.
    :param key: The key to decrypt with.
    :param nonce: The nonce to decrypt with.
    """
    # Validate parameters.
    if encrypted_data == None or key == None or nonce == None:
        raise ValueError("encrypted_data, key, and nonce cannot be None")
    if type(encrypted_data) == str:
        encrypted_data = encrypted_data.encode('utf-8')
    if type(encrypted_data) != bytes:
        raise ValueError("encrypted_data must be of type bytes")
    
    # Create cipher and decrypt data.
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_data)
    
    # Return the plaintext string.
    return plaintext