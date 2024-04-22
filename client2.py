import socket

# Tworzenie gniazda
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Pobieranie adresu IP i portu serwera
host = '192.168.0.139'
port = 12345

# Łączenie się z serwerem
client_socket.connect((host, port))

while True:
    # Wysyłanie danych do serwera
    message = input("Ja:")
    client_socket.send(message.encode())

    # Odbieranie odpowiedzi od serwera
    data = client_socket.recv(1024).decode()
    print("Serwer:", data)

# Zamykanie gniazda
client_socket.close()
