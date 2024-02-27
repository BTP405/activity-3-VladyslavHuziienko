# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import marshal
import types
import pickle
from multiprocessing import Process, Lock, Queue, current_process
import time

# Server's address and port
HOST = '127.0.0.1'
PORT = 9978

# Mutex to lock the queue
mutex = Lock()
# List to store the processes
processes = []

# Function to work with the client
def work_with_client(client_socket):
    # Receive the pickled data from the client
    print("Working with client ->", client_socket.getpeername(), "PID:", str(current_process().pid))
    data = client_socket.recv(9098)

    # Unpickle the data
    function_marshaled = pickle.loads(data)['function']
    args = pickle.loads(data)['args']

    # Unmarshal the function
    code = marshal.loads(function_marshaled)
    # Create the function
    function = types.FunctionType(code, globals(), "function")

    # Call the function with the arguments
    result = function(*args)
    # Pickle the result
    response = pickle.dumps({"result": result})

    # Send the pickled result to the client
    client_socket.sendall(response)
    print("Client ->", client_socket.getpeername(), "disconnected. \nData sent ->", result)
    client_socket.close()

# Worker process that take the client from the queue and process their request
def worker(clietns_queue):
    # Loop to wait for the clients without closing the process
    while True:
        # Get the client from the queue, protecting it with the mutex
        with mutex:
            # Get the client from the queue
            client_socket = clietns_queue.get()
            if client_socket:
                # If queue is not empty, work with the client
                work_with_client(client_socket)
            else:
                # If queue is empty, wait for 100ms to prevent too much CPU usage
                time.sleep(0.1)

# Function to start the worker processes
def start_workers(clietns_queue):
    # Create 5 worker processes (Can create any number of processes needed)
    for _ in range(5):
        # Create the process and start it
        process = Process(target=worker, args=(clietns_queue,))
        process.start()
        # Append the process to the list
        processes.append(process)

if __name__ == '__main__':
    # Create the queue to store the clients
    clietns_queue = Queue()

    # Initialize the server socket, listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)

    print(f"Server listening on {HOST}:{PORT}")

    # Start the worker processes
    start_workers(clietns_queue)

    # Loop to wait for the clients
    while True:
        try:
            # Accept the client
            client_socket, client_address = server_socket.accept()
            print(f"Connected to {client_address}")
            
            # Put the client in the queue, protecting it with the mutex
            with mutex:
                clietns_queue.put(client_socket)
        except Exception as e:
            print(f"Error: {e}")


    server_socket.close()