import socket
import threading

clients = []
clients_names = []


def receive_message(client_socket, address, name):
    print('Connected to', address)

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Disconnected from {name} {address}")
                break

            if ':' in data:
                broadcast_message(f'{data}'.encode('utf-8'))

        except Exception as e:
            clients.remove(client_socket)
            clients_names.remove(name)
            for client_socket in clients:
                try:
                    client_socket.send(f"-delete- {name}".encode('utf-8'))
                except Exception as e:
                    print("delete failed!", e)
            print(f"Disconnected from {name} {address}")
            break


def broadcast_message(message):
    # Wyślij wiadomość do wszystkich klientów
    for client_socket in clients:
        try:

            client_socket.send(message)
        except Exception as e:
            print("Error broadcasting message to a client:", e)


HOST = '0.0.0.0'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)  # Max 10 clients
print('listening on port...')
while True:
    comm, address = server.accept()  # tego używamy do komunikacji z klientem
    name = comm.recv(1024).decode('utf-8')
    clients.append(comm)
    clients_names.append(name)
    for client_socket in clients:
        try:

            client_socket.send(f'{','.join(clients_names)}'.encode('utf-8'))
        except Exception as e:
            print("user-list error", e)
    threading.Thread(target=receive_message, args=(comm, address, name)).start()
