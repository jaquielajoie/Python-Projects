import threading
import socket 

# Define socket host and port
SERVER_HOST = '127.0.0.1' # Localhost
SERVER_PORT = 9000

class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []

        # Create socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind socket to host and port
        self.s.bind((SERVER_HOST, SERVER_PORT))
        # Listen for connections
        self.s.listen(5) # 5 is the maximum number of queued connections we'll allow
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client_connection(self, client_socket):
        while True:
            try:
                # Receive the client's data
                request = client_socket.recv(1024)
                print(f"[*] Received {request.decode('ascii')}")
                # Send back a packet
                client_socket.send("ACK!".encode('ascii'))
                # Broadcast to all clients
                index = self.clients.index(client_socket)
                nickname = self.nicknames[index]
                # self.broadcast(f"{nickname}: {request.decode('ascii')}".encode('ascii'))
            except Exception as e:
                print(e)
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close() 
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                self.nicknames.remove(nickname)
                break
            
    def accept_connections(self):
        while True:
            # Accept client connection
            client_socket, client_address = self.s.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
            client_socket.send("NICK".encode('ascii'))
            nickname = client_socket.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client_socket) 
            print(f"[*] Nickname of the client is {nickname}")
            self.broadcast(f"{nickname} joined the chat!".encode('ascii'))
            client_socket.send("Connected to the server!".encode('ascii'))
            # Start handling thread for client
            thread = threading.Thread(target=self.handle_client_connection, args=(client_socket,))
            thread.start()

if __name__ == "__main__":
    server = SocketServer(SERVER_HOST, SERVER_PORT)
    server.accept_connections()