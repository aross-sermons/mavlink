from utils import encrypt_decrypt_aes as aes

key_size = 32
print(f'key_size: {key_size}')

iv_size = 16
print(f'iv_size: {iv_size}')

aes_key = aes.generate_aes_key(key_size)
print(f'aes_key: {aes_key}')

message = "This is a secret"
print(f'message: {message}')

encrypted_message = aes.encrypt_data(message, aes_key, iv_size)
print(f'encrypted_message: {encrypted_message}')

decrypted_message = aes.decrypt_data(encrypted_message, aes_key, iv_size)
print(f'decrypted_message: {decrypted_message}')