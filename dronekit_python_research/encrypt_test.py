from utils import encrypt_decrypt_aes as aes
from utils import encrypt_decrypt_chacha20 as chacha
from utils import encrypt_decrypt_tea as tea
from codecarbon import EmissionsTracker
from enum import Enum
import os
import time

class Method(Enum):
    AES_16 = 1
    AES_24 = 2
    AES_32 = 3
    CHACHA = 4
    TEA_16 = 5
    TEA_32 = 6
    TEA_64 = 7

MESSAGE_SHORT = "This is a secret."
MESSAGE_LONG = "This is a long secret. It is meant to simulate larger missions. You don't have to read this full text, but I applaud you if you do. What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Why do we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like). Where does it come from? Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of de Finibus Bonorum et Malorum (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, Lorem ipsum dolor sit amet.., comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from de Finibus Bonorum et Malorum by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham. Where can I get some? There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc."

def test_aes_16(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt.
    """
    # Set iv size
    iv_size = 16
    # Generate aes key
    aes_key = aes.generate_aes_key(key_size=16)
    # Encrypt message
    encrypted_message = aes.encrypt_data(data=message, key=aes_key, iv_size=iv_size)
    # Decrypt encrypted_message
    decrypted_message = aes.decrypt_data(encrypted_data=encrypted_message, key=aes_key, iv_size=iv_size)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_aes_24(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt.
    """
    # Set iv size
    iv_size = 16
    # Generate aes key
    aes_key = aes.generate_aes_key(key_size=24)
    # Encrypt message
    encrypted_message = aes.encrypt_data(data=message, key=aes_key, iv_size=iv_size)
    # Decrypt encrypted_message
    decrypted_message = aes.decrypt_data(encrypted_data=encrypted_message, key=aes_key, iv_size=iv_size)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_aes_32(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt.
    """
    # Set iv size
    iv_size = 16
    # Generate aes key
    aes_key = aes.generate_aes_key(key_size=32)
    # Encrypt message
    encrypted_message = aes.encrypt_data(data=message, key=aes_key, iv_size=iv_size)
    # Decrypt encrypted_message
    decrypted_message = aes.decrypt_data(encrypted_data=encrypted_message, key=aes_key, iv_size=iv_size)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_chacha(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt.
    """
    # Generate chacha20 key
    chacha_key = chacha.generate_key()
    # Encrypt message
    nonce, encrypted_message = chacha.encrypt_data(data=message, key=chacha_key)
    # Decrypt message
    decrypted_message = chacha.decrypt_data(nonce=nonce, encrypted_data=encrypted_message, key=chacha_key)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_tea_16(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt
    """
    # Generate tea key
    tea_key = tea.generate_key()
    # Encrypt message
    encrypted_message = tea.encrypt_data(data=message, key=tea_key, num_rounds=16)
    # Decrypt message
    decrypted_message = tea.decrypt_data(data=encrypted_message, key=tea_key, num_rounds=16)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_tea_32(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt
    """
    # Generate tea key
    tea_key = tea.generate_key()
    # Encrypt message
    encrypted_message = tea.encrypt_data(data=message, key=tea_key, num_rounds=32)
    # Decrypt message
    decrypted_message = tea.decrypt_data(data=encrypted_message, key=tea_key, num_rounds=32)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def test_tea_64(message):
    """
    Encrypts and decrypts the given message.

    :param message: The message to encrypt
    """
    # Generate tea key
    tea_key = tea.generate_key()
    # Encrypt message
    encrypted_message = tea.encrypt_data(data=message, key=tea_key, num_rounds=64)
    # Decrypt message
    decrypted_message = tea.decrypt_data(data=encrypted_message, key=tea_key, num_rounds=64)
    # Return encrypted and decrypted messages
    return encrypted_message, decrypted_message

def log_times(methods:list[Method], message:str, repeat:int):
    """
    Logs the length of time it takes to ecomplete [repeat] encryption/decrytion cycles
    with the given message using the given methods.
    
    :param methods: A list of the methods to use, taken from enumerated class Method.
    :param message: The message to use. Pregenerated global messages are MESSAGE_SHORT and MESSAGE_LONG.
    :param repeat: The number of times to repeat each encryption/decryption cycle.
    """

    # Define a dictionary mapping methods to functions.
    encryption_methods = {
        Method.AES_16: test_aes_16,
        Method.AES_24: test_aes_24,
        Method.AES_32: test_aes_32,
        Method.CHACHA: test_chacha,
        Method.TEA_16: test_tea_16,
        Method.TEA_32: test_tea_32,
        Method.TEA_64: test_tea_64
    }

    # Set carbon tracker
    tracker = EmissionsTracker()
    emissions_data_list = []

    # For each method listed in methods
    for method in methods:
        print("#############################################################################")
        print(f'Testing with method {method.name} for {repeat} times.')
        # Run the encryption method for the given number of times.
        for i in range(1, (repeat+1)):
            print("-------------------------------------------------------------------------")
            print(f'Method {method.name}, {i}/{repeat}:')
            # Call the appropriate encryption method
            if method in encryption_methods:
                # Start emissions tracker and record start time
                tracker.start()
                start_time = time.perf_counter()
                encrypted_message, decrypted_message = encryption_methods[method](message)
                # Stop emissions tracker and record end time
                tracker.stop()
                end_time = time.perf_counter()
                total_time = end_time - start_time
                # Print messages
                print(f'Encrypted Message Preview: {encrypted_message[:10]}')
                print(f'Decrypted Message Preview: {decrypted_message[:10]}')
                # Retrieve emissions data and append encryption method name
                emissions_data_dict = vars(tracker._prepare_emissions_data())
                emissions_data = ','.join(str(value) for value in emissions_data_dict.values())
                emissions_data = emissions_data + "," + method.name + "," + str(total_time)
                emissions_data_list.append(emissions_data)
                print("Successfully logged encryption-decryption.")
            else:
                raise ValueError("Unknown encryption method")
            
            print("Finished")
            print("-------------------------------------------------------------------------")
        print("#############################################################################")
        
    # Insert header names into emissions_data_list
    header_names = list(emissions_data_dict.keys()) + ["method"] + ["total_time"]
    emissions_data_list.insert(0, ','.join(header_names))
    
    # Find the last log file so a new log file can be created.
    log_num = 1
    while os.path.exists(f'./logs/encryption_decryption_log{log_num}.csv'):
        log_num += 1

    # Create a new log file and write emissions data.
    with open(f'./logs/encryption_decryption_log{log_num}.csv', 'w') as new_file:
        for data in emissions_data_list:
            new_file.write(data + "\n")

if __name__ == "__main__":
    methods = [Method.AES_16, Method.AES_24, Method.AES_32, Method.CHACHA, Method.TEA_16, Method.TEA_32, Method.TEA_64]
    log_times(methods=methods, message=MESSAGE_LONG, repeat=20)