from dronekit import connect, VehicleMode, mavutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# AES key generated from aes.py. Should be replaced with automatic generation.
aes_key = b"X\xd0\xf2Zl\xe2\xc3j\x9fW\xc4\xf0\x87\x88\x07\xdd\xe01'.\x80\x9fu\xf8\x01M\x94\x8a\xc2\xb7cN"

def decrypt_message(aes_key, ciphertext):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

def message_listener(self, name, message):
    if name == 'RAW_DATA':
        encrypted_message = message.data
        decrypted_message = decrypt_message(aes_key, encrypted_message)

        mav = mavutil.mavlink.MAVLink(None)
        decoded_message = mav.decode(decrypted_message)
        print("Recieved MACLink message:", decoded_message)

connection_string = 'tcp:127.0.0.1:5760'
vehicle = connect(connection_string, wait_ready=True)

vehicle._handler.add_raw_data_listener(message_listener)

import time
while True:
    time.sleep(1)