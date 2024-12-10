import socket
import select

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def broadcast(sender_sock, message):
    """Send a message to all clients except the sender."""
    for client in clients[:]:  # Make a copy of the clients list to avoid modification during iteration
        if client != sender_sock and client != server_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message to a client: {e}")
                remove_client(client)

def remove_client(client_sock):
    """Remove a client from the list and close the connection."""
    if client_sock in clients:
        try:
            client_address = client_sock.getpeername()  # Get the address before removing the client
            print(f"Client {client_address} removed.")
            clients.remove(client_sock)
            client_sock.close()
            return client_address  # Return the address for future use
        except Exception as e:
            print(f"Error removing client: {e}")
            return None
    return None

# Setup server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = [server_socket]

print(f"Chat server started on {SERVER_HOST}:{SERVER_PORT}")

try:
    while True:
        ready_to_read, _, _ = select.select(clients, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                client_sock, client_address = server_socket.accept()
                clients.append(client_sock)
                print(f"Client {client_address} connected.")
                broadcast(client_sock, f"Client {client_address} has joined the chat.\n".encode('utf-8'))
            else:
                try:
                    message = sock.recv(BUFFER_SIZE)
                    if message:
                        print(f"Message from {sock.getpeername()}: {message.decode('utf-8')}")
                        broadcast(sock, message)
                    else:  # Client disconnected
                        client_address = remove_client(sock)
                        if client_address:
                            broadcast(sock, f"Client {client_address} has left the chat.\n".encode('utf-8'))
                except Exception as e:
                    client_address = remove_client(sock)
                    if client_address:
                        print(f"Error with client {client_address}: {e}")
except KeyboardInterrupt:
    print("Shutting down server.")
    for client in clients:
        client.close()
finally:
    server_socket.close()
