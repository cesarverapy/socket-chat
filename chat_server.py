import socket
import select

# server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def broadcast(sender_sock, message):
    """send a message to all clients except the sender."""
    for client in clients:
        if client != sender_sock:
            try:
                client.send(message)
            except Exception as e:
                print(f"error sending message: {e}")
                remove_client(client)

def remove_client(client_sock):
    """remove a client from the list and close the connection."""
    if client_sock in clients:
        clients.remove(client_sock)
        client_sock.close()

# setup server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = [server_socket]

print(f"chat server started on {SERVER_HOST}:{SERVER_PORT}")

try:
    while True:
        ready_to_read, _, _ = select.select(clients, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                client_sock, client_address = server_socket.accept()
                clients.append(client_sock)
                print(f"client {client_address} connected.")
                broadcast(client_sock, f"client {client_address} has joined the chat.\n".encode('utf-8'))
            else:
                try:
                    message = sock.recv(BUFFER_SIZE)
                    if message:
                        broadcast(sock, message)
                    else:
                        print(f"client {sock.getpeername()} disconnected.")
                        remove_client(sock)
                        broadcast(sock, f"client {sock.getpeername()} has left the chat.\n".encode('utf-8'))
                except Exception as e:
                    print(f"error with client {sock.getpeername()}: {e}")
                    remove_client(sock)
except KeyboardInterrupt:
    print("shutting down server.")
    for client in clients:
        client.close()
finally:
    server_socket.close()
