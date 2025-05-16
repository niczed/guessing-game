import socket

class GuessingGameBot:
    def __init__(self, host="127.0.0.1", port=7777, password="guessme"):
        self.host = host
        self.port = port
        self.password = password

    def play(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                print("Connecting to server...")
                client_socket.connect((self.host, self.port))
                print("Connected to the server.")

                print("Waiting for server message...")
                server_message = client_socket.recv(1024).decode()
                print(f"Server message: {server_message.strip()}")
              
                client_socket.sendall(self.password.encode())
                auth_response = client_socket.recv(1024).decode()
                print(f"Authentication response: {auth_response.strip()}")
              
                if "Incorrect password" in auth_response:
                    print("Authentication failed. Exiting...")
                    return
        
                low, high = 1, 100
                while True:
                   
                    guess = (low + high) // 2
                    print(f"Bot guesses: {guess}")
                    client_socket.sendall(str(guess).encode())

                    response = client_socket.recv(1024).decode().strip()
                    print(f"Server response: {response}")
                    
                    if "Too low!" in response:
                        low = guess + 1
                    elif "Too high!" in response:
                        high = guess - 1
                    elif "Correct!" in response:
                        print("Game over !! Bot won!")
                        break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    bot = GuessingGameBot()
    bot.play()
