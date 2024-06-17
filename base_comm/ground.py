from os import urandom
from dronekit import connect, VehicleMode, mavutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# AES key generated from aes.py. Should be replaced with automatic generation.
aes_key = b"X\xd0\xf2Zl\xe2\xc3j\x9fW\xc4\xf0\x87\x88\x07\xdd\xe01'.\x80\x9fu\xf8\x01M\x94\x8a\xc2\xb7cN"

# Encrypt message using AES
def encrypt_message(aes_key, plaintext):
	iv = urandom(16)
	cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
	encryptor = cipher.encryptor()

	padder = padding.PKCS7(128).padder()
	padded_data = padder.update(plaintext) + padder.finalize()

	ciphertext = encryptor.update(padded_data) + encryptor.finalize()
	return iv + ciphertext

# Send encrypted message over MAVLink
def send_encrypted_heartbeat(vehicle):
	heartbeat_msg = vehicle.message_factory.heartbeat_encode(
        mavutil.mavlink.MAV_TYPE_QUADROTOR, 
        mavutil.mavlink.MAV_AUTOPILOT_GENERIC, 
        0, 0, 0, 0
		)
	packed_msg = heartbeat_msg.pack(vehicle._handler)

	encrypted_message = encrypt_message(aes_key, packed_msg)

	vehicle._handler.write(encrypt_message)
	print(encrypted_message.hex())

connection_string = 'tcp:127.0.0.1:7560'
vehicle = connect(connection_string, wait_ready=True)

send_encrypted_heartbeat(vehicle)

vehicle.close()