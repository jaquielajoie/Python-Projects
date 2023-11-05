import threading
import socket

# Define socket host and port
SERVER_HOST = '127.0.0.1' # Localhost
SERVER_PORT = 9000

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.nick = input("Choose your nickname: ")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server
        self.s.connect((SERVER_HOST, SERVER_PORT))

    def receive_message(self):
        while True:
            try:
                # Receive message from server
                message = self.s.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.s.send(self.nick.encode('ascii'))
                else:
                    print(f'{message}')
            except Exception as e:
                # Close connection when error
                print(e)
                print("An error occured! receive_message")
                self.s.close()
                break

    def send_message(self):
        while True:
            try:
                # Send message to server
                message = f'{self.nick}: {input("Type your message:")}'
                self.s.send(message.encode('ascii'))
            except Exception as e:
                # Close connection when error
                print(e)
                print("An error occured! send_message")
                self.s.close()
                break

    def run(self):
        # Create threads for sending and receiving messages
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()
        send_thread = threading.Thread(target=self.send_message)
        send_thread.start()

if __name__ == "__main__":
    client = SocketClient(SERVER_HOST, SERVER_PORT)
    client.run()