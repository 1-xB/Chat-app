import socket
import threading

def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            print(data)
        except Exception as e:
            print("Błąd:", e)
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.0.139'
port = 12345

while True:
    name = input("Podaj swoją nazwę: ")
    if name:
        break

client_socket.connect((host, port))
client_socket.send(name.encode())

receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
receive_thread.start()

while True:
    message = input("Ja: ")
    if message:
        client_socket.send(message.encode())

client_socket.close()
