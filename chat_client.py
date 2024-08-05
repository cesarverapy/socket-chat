import socket
import threading
import sys

# Configuración del cliente
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(sock):
    """funcion para recibir mensajes del servidor"""
    while True:
        try:
            message = sock.recv(BUFFER_SIZE)
            if message:
                print(message.decode())
            else:
                sock.close()
                break
        except:
            print("conexion cerrada por el servidor")
            sock.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

print("conectado, envia un mensaje")

# Hilo para recibir mensajes
threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    try:
        message = input()
        if message.lower() == 'exit':
            client_socket.send("cliente ha salido del chat.".encode())
            client_socket.close()
            sys.exit()
        client_socket.send(message.encode())
    except KeyboardInterrupt:
        print("saliendo del chat")
        client_socket.close()
        sys.exit()
