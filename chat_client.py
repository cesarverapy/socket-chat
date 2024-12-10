import socket
import threading
import sys

# Client configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(sock):
    """Receive messages from the server."""
    while True:
        try:
            message = sock.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                print(message)
            else:
                print("Disconnected from server.")
                sock.close()
                sys.exit()
        except Exception as e:
            print(f"Error receiving message: {e}")
            sock.close()
            sys.exit()

# Setup client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

print("Connected to the chat server. Type 'exit' to leave.")

# Start thread to handle incoming messages
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.daemon = True
thread.start()

try:
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.send("Client has left the chat.".encode('utf-8'))
            print("Exiting chat...")
            client_socket.close()
            sys.exit()
        client_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\nDisconnected.")
    client_socket.close()
    sys.exit()
