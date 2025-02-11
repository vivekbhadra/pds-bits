#!/usr/bin/env python
# client.py
import socket

def main():
    host = "localhost"
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Client: Connected to server. Type your messages. Type 'exit' to quit.")

    try:
        while True:
            msg = input("Client: Enter message: ")
            client_socket.sendall(msg.encode())
            if msg.lower() == "exit":
                break
            # Receive acknowledgment from the server
            data = client_socket.recv(1024).decode()
            print("Server:", data.strip())
    except KeyboardInterrupt:
        print("Client: Interrupted. Exiting.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
