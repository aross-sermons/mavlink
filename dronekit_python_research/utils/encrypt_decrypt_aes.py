from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generate_aes_key(key_size:int=32):
    """
    Returns a generated aes key of key_size.

    :param key_size: The size of the aes key to generate.
    :return: The aes key.
    """
    if key_size not in [16, 24, 32]:
        raise ValueError("Key size must be 16, 24, or 32 bytes.")
    return urandom(key_size)

def write_aes_to_file(filename:str, key:bytes, iv_size:int):
    """
    
    """
    with open(filename, 'w') as file:
        file.write(f'{len(key)},{iv_size},{key.hex()}')

def read_aes_from_file(filename:str):
    """
    
    """
    with open(filename, 'r') as file:
        data = file.readline().strip()

    key_length, iv_length, key_hex = data.split(',')
    key_bytes = bytes.fromhex(key_hex)

    return int(key_length), int(iv_length), key_bytes

def encrypt_data(data:bytes, key:bytes, iv_size:int=16) -> bytes:
    """
    Encrypts the given data.

    :param data: The data to encrypt.
    :param key: The key to use.
    :param iv_size: The iv_size to use.
    :return: The encrypted data.
    """
    if data == None or key == None:
        raise ValueError("data and key cannot be None")
    if type(data) == str:
        data = data.encode('utf-8')
    if type(data) != bytes:
        raise ValueError("data must be of type bytes")
    
    iv = urandom(iv_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    return(iv + encrypted_data)

def decrypt_data(encrypted_data: bytes, key: bytes, iv_size:int=16) -> bytes:
    """
    Decrypts the given encrypted_data.

    :param encrypted_data: The data to decrypt.
    :param key: The key to use.
    :param iv_size: The iv_size to use.
    :return: The decrypted data.
    """
    if encrypted_data == None or key == None:
        raise ValueError("Data and key cannot be None")
    if type(encrypted_data) == str:
        encrypted_data = encrypted_data.encode('utf-8')
    if type(encrypted_data) != bytes:
        raise ValueError("encrypted_data must be of type bytes")

    iv = encrypted_data[:iv_size]
    cipherdata = encrypted_data[iv_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return(unpad(cipher.decrypt(cipherdata), AES.block_size))