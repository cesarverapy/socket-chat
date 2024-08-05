import socket
import select

# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def broadcast(sock, message):
    """envia el mensaje a todos los clientes conectados excepto el remitente"""
    for client_socket in clients:
        if client_socket != server_socket and client_socket != sock:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                clients.remove(client_socket)

# Crear socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(10)

clients = []
clients.append(server_socket)

print(f"servidor de chat iniciado en {SERVER_HOST}:{SERVER_PORT}")

while True:
    read_sockets, _, error_sockets = select.select(clients, [], clients)

    for sock in read_sockets:
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            print(f"el cliente {client_address} se ha conectado")
            broadcast(client_socket, f"el cliente {client_address} ha entrado al chat\n".encode())
        else:
            try:
                data = sock.recv(BUFFER_SIZE)
                if data:
                    broadcast(sock, data)
                else:
                    if sock in clients:
                        clients.remove(sock)
                    broadcast(sock, f"el cliente {sock.getpeername()} salio el chat\n".encode())
            except:
                broadcast(sock, f"el cliente {sock.getpeername()} salio el chat\n".encode())
                continue

    for sock in error_sockets:
        if sock in clients:
            clients.remove(sock)
            broadcast(sock, f"el cliente {sock.getpeername()} salio sel chat\n".encode())
