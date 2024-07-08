from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Set plaintext message
plaintext = b'This is a secret message'
print("Plaintext message: ", plaintext)

# Generate an AES key
key = get_random_bytes(16) # AES-128 bit key

# Use the AES key to generate an encrypted message
iv = get_random_bytes(16) # Initialization vector
cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
print("Encrypted message: ", ciphertext)

# Use the AES key to decrypt the message
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)

print("Decrypted message: ", decrypted_message.decode())