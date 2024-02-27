# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import pickle

# Directory to save the files
FILES_DIR = './server_files'

# Server's address and port
HOST = '127.0.0.1'
PORT = 9900

# Initialize the server socket, bind, and start listening for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Loop to work with the clients without closing the server
while True:
    # Accept the client's connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # Try/except block to handle errors that may occur during the connection, and transfer
    try:
        # Receive the pickled data from the client
        data = client_socket.recv(1048576)

        # Unpickle the data
        file_data = pickle.loads(data)['data']
        file_name = pickle.loads(data)['name']

        # Save the file
        file = open(f"{FILES_DIR}/{file_name}", 'wb')
        file.write(file_data)
        file.close()
        print("Received file")

        # Send a response to the client
        client_socket.sendall(b"File received")
    except Exception as e:
        print(f"Error: {e}")
    
    client_socket.close()

server_socket.close()