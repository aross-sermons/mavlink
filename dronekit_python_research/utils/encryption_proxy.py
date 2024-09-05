from utils import encrypt_decrypt_aes as aes
import socket
import select

def proxy_server(server_connection_string, base_connection_string, remote_connection_string, aes_key_filename):
    """
    A proxy server meant to recieve and send encrypted messages from the server at sender_connection_string.

    
    """
    # Split connection strings for socket.
    server_host, server_port = server_connection_string.split(':')
    base_host, base_port = base_connection_string.split(':')
    remote_host, remote_port = base_connection_string.split(':')

    # Read and store aes key info.
    key_length, iv_length, key = aes.read_aes_from_file(aes_key_filename)

    # Set up the server socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_host, int(server_port))
        server_socket.listen(1)
        print(f'Proxy server listening on {server_connection_string}')

        # Declare connection objects.
        base_conn = None
        remote_conn = None

        # Wait until both connections are satisfied.
        while not (base_conn and remote_conn):
            conn, addr = server_socket.accept()
            client_ip, client_port = addr
            # Match the client connection to the base or remote.
            if client_ip == base_host and client_port == base_port:
                base_conn = conn
                print(f'Connected to base at {addr}')
            elif client_ip == remote_host and client_port == remote_port:
                remote_conn = conn
                print(f'Connected to remote at {addr}')
            else:
                conn.close()
                print(f'Rejected connection from {addr}')

        # Infinite loop for relaying data between the base and remote.
        while True:
            # Use select to wait for data from either base or remote.
            readable, _, _ = select.select([base_conn, remote_conn], [], [])

            for sock in readable:
                if sock == base_conn:
                    # Read data from base, encrypt it, and send to remote.
                    base_data = base_conn.recv(4096)
                    if base_data:
                        encrypted_data = aes.encrypt_data(base_data, key, iv_length)
                        remote_conn.sendall(encrypted_data)
                elif sock == remote_conn:
                    # Read data from remote, decrypt it, and send to base.
                    remote_data = remote_conn.recv(4096)
                    if remote_data:
                        decrypted_data = aes.decrypt_data(remote_data, key, iv_length)
                        base_conn.sendall(decrypted_data)