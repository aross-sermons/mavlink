from utils import encrypt_decrypt as ed

message = "this is a secret"
print(f'Message: {message}')

aes = ed.generate_aes_key()
print(f'AES: {aes}')

encrypted = ed.encrypt_str(message, aes)
print(f'Encrypted: {encrypted}')

decrypted = ed.decrypt_str(encrypted, aes)
print(f'Decrypted: {decrypted}')
