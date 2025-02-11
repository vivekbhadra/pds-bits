#!/usr/bin/env python 
# xmlrpc_message_server.py

from xmlrpc.server import SimpleXMLRPCServer

# --- Function to Process Client Messages ---
def process_client_message(client_message):
    """
    Processes a message received from the client.
    For demonstration, appends a note and returns the modified message.
    This function runs in the same process as the XML-RPC server.
    """
    print("Received message: ", client_message)  # Log received message
    return f"{client_message} [Processed by RPC Server]"

# --- Function to Start the XML-RPC Server ---
def start_rpc_server():
    """
    Initializes and starts the XML-RPC server to handle remote function calls.
    The server listens on localhost:8000 and handles one request at a time.
    """
    rpc_server = SimpleXMLRPCServer(("localhost", 8000), logRequests=True, allow_none=True)
    print("XML-RPC Server is running on port 8000...")
    
    # Register the process_client_message function as a remote procedure
    rpc_server.register_function(process_client_message, "process_client_message")
    
    # Keep the server running indefinitely to handle incoming requests
    rpc_server.serve_forever()

# --- Entry Point ---
if __name__ == "__main__":
    start_rpc_server()  # Start the XML-RPC server

