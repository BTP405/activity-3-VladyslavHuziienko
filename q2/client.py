# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import marshal
import pickle
import time

# Test functions that will be sent to the server
def test1():
    return 1
def test2(x):
    return x*x
def test3(x, y):
    result = 1
    for i in range(x):
        result += y**i
    return result

# Server's address and port
HOST = '127.0.0.1'
PORT = 9978

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try/except block to handle errors that may occur
try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print('Connected to the server')

    timer = time.time()

    # Pickle and marshal function with the arguments
    function_with_args = pickle.dumps({"function": marshal.dumps(test3.__code__), "args": [10, 10]})

    # Send the pickled function to the server
    client_socket.sendall(function_with_args)

    # Receive the server's response
    data = client_socket.recv(1024)
    result = pickle.loads(data)['result']
    print('Result:', result)
    print('Time:', time.time() - timer)
except Exception as e:
    print('Error:', e)

client_socket.close()
print('Socket closed')
