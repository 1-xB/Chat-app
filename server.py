import socket
import threading

clients = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(clients[client_socket], client_address,  ":", data)
            for client in clients:
                if client != client_socket:
                    client.send((clients[client_socket]  + ": " + data).encode())
        except Exception as e:
            print("Błąd:", e)
            del clients[client_socket]
            break
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
port = 12345

server_socket.bind((host, port))
server_socket.listen(5)
print("Serwer nasłuchuje na porcie", port)

while True:
    client_socket, client_address = server_socket.accept()
    name = client_socket.recv(1024).decode()
    clients[client_socket] = name
    print("Połączono z", client_address, "jako", name)

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
