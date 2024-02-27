# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import pickle

# File to be transfered
FILE_PATH = input('Enter the file path: ')

# Check if the file exists
try:
    file = open(FILE_PATH, 'rb')
    file.close()
except:
    print('File does not exist')
    exit()

# Server's address and port
HOST = '127.0.0.1'
PORT = 9900

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try/except block to handle errors that may occur during the connection, and transfer
try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print('Connected to the server')

    # Open the file, read its data, and pickle it
    file = open(FILE_PATH, 'rb')
    file_data = file.read()
    file_name = file.name.split('/')[-1]
    file.close()

    pickled_file = pickle.dumps({"name": file_name, "data": file_data})

    # Send the pickled file to the server
    client_socket.sendall(pickled_file)

    # Receive the server's response
    data = client_socket.recv(1024)
    print('Received:', data.decode())
except Exception as e:
    print('Error:', e)

# Close the socket
client_socket.close()
print('Socket closed')