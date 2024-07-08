from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Set plaintext message
plaintext = b'This is a secret message'
print("Plaintext message: ", plaintext)

# Generate a local AES key
key = get_random_bytes(16)  # AES-128 bit key

# Use the AES key to generate an encrypted message
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

print("Encrypted message: ", ciphertext)

# Use the AES key to decrypt the message
cipher = AES.new(key, AES.MODE_GCM, cipher.nonce)
decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)

print("Decrypted message:", decrypted_message.decode())