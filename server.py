import random
import socket

class GuessingGameServer:
    def __init__(self, host="127.0.0.1", port=7777, password="StanTwice"):
        self.host = host
        self.port = port
        self.password = password  
        self.secret_number = random.randint(1, 100)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                
                conn.sendall(b"Enter the password to start the game: ")
                client_password = conn.recv(1024).decode().strip()
                if client_password != self.password:
                    conn.sendall(b"Incorrect password. Connection closing...\n")
                    conn.close()
                    continue

                conn.sendall(b"Access granted! Welcome to the Guessing Game.\n")
           
                attempts = 0
                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    try:
                        guess = int(data)
                        attempts += 1
                        if guess < self.secret_number:
                            response = "Too low!"
                        elif guess > self.secret_number:
                            response = "Too high!"
                        else:
                          
                            if attempts <= 5:
                                rating = "Excellent"
                            elif 6 <= attempts <= 20:
                                rating = "Very Good"
                            else:
                                rating = "Good / Fair"
                            response = f"Correct! You win! Attempts: {attempts}. Rating: {rating}\n"
                            conn.sendall(response.encode())
                           
                            self.secret_number = random.randint(1, 100)
                            attempts = 0
                            continue
                        conn.sendall(response.encode())
                    except ValueError:
                        conn.sendall(b"Invalid input! Please enter a number.\n")

    def stop(self):
        self.server_socket.close()

def main():
    server = GuessingGameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()
