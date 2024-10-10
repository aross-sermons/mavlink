import struct
from os import urandom

def generate_key() -> bytes:
    """
    Generates a random key for tea encryption.

    :return: A 16-byte key
    """
    return urandom(16)

def prepare_data(data:bytes) -> bytes:
    """
    Check data to be encyrpted to ensure that...
        1. The data is of type bytes (if string, converts to bytes)
        2. The data is properly padded

    :param data" The data to prepare
    :return: The prepared data
    :raises ValueError: If data is not of type string or bytes
    """
    # If data is a string, convert to bytes
    if isinstance(data, str):
        data = data.encode('utf-8')
    # If data is not bytes, raise ValueError
    elif not isinstance(data, bytes):
        raise ValueError("Data must be of type string or bytes")
    
    # If data is not a multiple of 8 bytes
    if len(data) % 8 != 0:
        padding_needed = 8 - (len(data) % 8)
        data += b' ' * padding_needed  # Padding with spaces
    
    # Return the data as padded bytes
    return data

def encrypt_data(data:bytes, key:bytes, delta:int=0x9e3779b9, num_rounds:int=32) -> bytes:
    """
    Encrypts the given data using TEA.

    :param data: The data to encrypt (bytes or string)
    :param key: The key to encrypt with, must be 16 bytes long
    :param delta: The delta constant used in TEA
    :param num_rounds: The number of rounds to perform
    :return: The encrypted data as bytes
    """
    # Prepare the data with byte-conversion and padding
    plaintext = prepare_data(data)

    # Encrypt data
    encrypted_data = b''
    for i in range(0, len(plaintext), 8):
        v0, v1 = struct.unpack('!2L', plaintext[i:i+8])
        k0, k1, k2, k3 = struct.unpack('!4L', key[:16])
    
        sum = 0
        for _ in range(num_rounds):
            # Increment sum by delta each round
            sum = (sum + delta) & 0xffffffff

            # Update v0:
            # - v0                 -> The value to be updated
            # - + ((v1 << 4) + k0) -> add ((left shift of v1 by 4) + k0)
            # - ^ (v1 + sum)       -> add sum
            # - ^ ((v1 >> 5) + k1) -> add ((right shift of v1 by 5) + k1)
            # - & 0xFFFFFFFF       -> mask to 32-bit integer
            v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xffffffff

            # Update v1:
            # - v1                 -> The value to be updated
            # - + ((v0 << 4) + k2) -> add ((left shift of v0 by 4) + k2)
            # - ^ (v0 + sum)       -> add sum
            # - ^ ((v0 >> 5) + k3) -> add ((right shift of v0 by 5) + k3)
            # - & 0xFFFFFFFF       -> mask to 32-bit integer
            v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xffffffff

        encrypted_data += struct.pack('!2L', v0, v1)

    # Return the encrypted data
    return encrypted_data

def decrypt_data(data:bytes, key:bytes, delta:int=0x9e3779b9, num_rounds:int=32) -> bytes:
    """
    Decrypts the given data using TEA.

    :param data: The data to decrypt (bytes)
    :param key: The key to decrypt with, must be 16 bytes long
    :param delta: The delta constant used in TEA
    :param num_rounds: The number of rounds to reverse
    :return: The decrypted data as bytes
    """
    # Ensure the key is properly formatted to 16 bytes and unpacked
    decrypted_data = b''
    
    for i in range(0, len(data), 8):
        v0, v1 = struct.unpack('!2L', data[i:i+8])
        k0, k1, k2, k3 = struct.unpack('!4L', key[:16])
    
        # Initialize sum to the maximum value before the loop
        sum = (delta * num_rounds) & 0xffffffff
        
        # Reverse the encryption rounds
        for _ in range(num_rounds):
            # Update v1:
            # - v1                 -> The value to be updated
            # - - ((v0 << 4) + k2) -> subtract ((left shift of v0 by 4) + k2)
            # - ^ (v0 + sum)       -> subtract sum
            # - ^ ((v0 >> 5) + k3) -> subtract ((right shift of v0 by 5) + k3)
            # - & 0xFFFFFFFF       -> mask to 32-bit integer
            v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xffffffff

            # Update v0:
            # - v0                 -> The value to be updated
            # - - ((v1 << 4) + k0) -> subtract ((left shift of v1 by 4) + k0)
            # - ^ (v1 + sum)       -> subtract sum
            # - ^ ((v1 >> 5) + k1) -> subtract ((right shift of v1 by 5) + k1)
            # - & 0xFFFFFFFF       -> mask to 32-bit integer
            v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xffffffff
            
            # Decrement sum by delta each round
            sum = (sum - delta) & 0xffffffff

        decrypted_data += struct.pack('!2L', v0, v1)

    # Remove trailing spaces
    decrypted_data = decrypted_data.rstrip(b' ')

    # Return the decrypted data
    return decrypted_data