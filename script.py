import socket
import threading

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    clients = []
    usernames = {}

    def broadcast(message, client_socket):
        for client in clients:
            if client != client_socket:
                client.send(message)

    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                broadcast(message, client_socket)
            except:
                index = clients.index(client_socket)
                clients.remove(client_socket)
                username = usernames[client_socket]
                broadcast(f'{username} has left the chat.'.encode('utf-8'), client_socket)
                del usernames[client_socket]
                client_socket.close()
                break

    def receive_connections():
        print(f'Server started at {host}:{port}')
        while True:
            client_socket, client_address = server.accept()
            print(f'New connection from {client_address}')

            client_socket.send('USERNAME'.encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8')
            usernames[client_socket] = username
            clients.append(client_socket)

            print(f'Username of the client is {username}')
            broadcast(f'{username} has joined the chat!'.encode('utf-8'), client_socket)
            client_socket.send('Connected to the server.'.encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

    receive_connections()

def start_client(server_ip, server_port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    username = input('Enter your username: ')
    
    def receive_messages():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message != 'USERNAME':
                    print(message)
            except:
                print('An error occurred!')
                client.close()
                break

    def send_message():
        while True:
            message = input("")
            client.send(f'{username}: {message}'.encode('utf-8'))

    client.send(username.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_message)
    send_thread.start()

def main():
    mode = input("Type 'server' to start the server or 'client' to start the client: ").strip().lower()
    if mode == 'server':
        host = socket.gethostbyname(socket.gethostname())  # Verwenden Sie die eigene IP-Adresse
        port = input("Enter the port to host the server on (leave blank for 12345): ").strip()
        port = int(port) if port else 12345
        print(f"Hosting on IP: {host}")
        start_server(host, port)
    elif mode == 'client':
        server_ip = input("Enter the server IP address to connect to: ").strip()
        server_port = input("Enter the server port to connect to (leave blank for 12345): ").strip()
        server_port = int(server_port) if server_port else 12345
        start_client(server_ip, server_port)
    else:
        print("Invalid option. Please type 'server' or 'client'.")

if __name__ == "__main__":
    main()
