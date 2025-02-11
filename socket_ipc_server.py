#!/usr/bin/env python
# ipc_socket_server.py
import socket
import multiprocessing
import time
import xmlrpc.client

# --- Message Processor (Consumer) ---
def message_reading_process(pipe_read_end):
    """
    Reads messages from the pipe, processes them (e.g., converts to uppercase and adds timestamp),
    then calls the RPC service for additional processing.
    """
    rpc_client = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)
    
    while True:
        message = pipe_read_end.recv()  # Blocking call to receive a message from the producer
        if message == "QUIT":
            print("Processor: Shutting down.")
            break

        # Local processing: uppercase conversion and adding a timestamp
        processed_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message.upper()}"
        print(f"Processor: Processed message: {processed_message}")

        # Send the processed message to the RPC service
        try:
            rpc_response = rpc_client.process_client_message(processed_message)
            print(f"Processor: RPC response: {rpc_response}")
        except Exception as error:
            print(f"Processor: RPC call failed: {error}")

# --- Client Connection Handler (Producer) ---
def handle_client(client_socket, pipe_write_end):
    """
    Handles client connection: receives data via socket,
    and sends it through the IPC pipe for processing.
    """
    with client_socket:
        print("Handler: Client connected.")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # Client disconnected
            
            message = data.decode().strip()
            if message.lower() == "exit":
                pipe_write_end.send("QUIT")  # Signal message_reading_process to exit
                print("Handler: Received shutdown command from client.")
                break
            
            print(f"Handler: Received message: {message}")
            pipe_write_end.send(message)  # Send message to message_reading_process via IPC
            client_socket.sendall("Message received and is being processed.\n".encode())
    print("Handler: Client disconnected.")

# --- TCP Server ---
def start_tcp_server(pipe_write_end):
    """
    Initializes and runs the TCP socket server.
    Handles each client connection by delegating it to a handler.
    """
    server_host = "localhost"
    server_port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server: Listening on {server_host}:{server_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Server: Connection from {client_address}")
        handle_client(client_socket, pipe_write_end)
    
    server_socket.close()

# --- Main Entry Point ---
def main():
    """
    Sets up IPC and starts the message message_reading_process and TCP server.
    """
    pipe_write_end, pipe_read_end = multiprocessing.Pipe()
    
    message_reader_process = multiprocessing.Process(target=message_reading_process, args=(pipe_read_end,))
    message_reader_process.start()
    
    try:
        start_tcp_server(pipe_write_end)
    except KeyboardInterrupt:
        print("Server: Shutting down.")
    finally:
        pipe_write_end.send("QUIT")
        message_reader_process.join()

if __name__ == "__main__":
    main()

