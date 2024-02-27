# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import threading
import pickle
import queue

# Server's address and port
HOST = '127.0.0.1'
PORT = 9978

# Mutex to lock the clients list
clients_mutex = threading.Lock()
# Mutex to lock the queue
queue_mutex = threading.Lock()

# List to store the clients
clients = []
# Queue to store the messages to be broadcasted
broadcast_queue = queue.Queue()

# Function to work with the client
def handle_client(client_socket):
    # Receive the client's name
    client_name = client_socket.recv(1024)
    client_name = pickle.loads(client_name)

    print(f"Client connected: {client_name}")

    # Put client connect message to the broadcast queue
    connect_message = f"{client_name} has joined the chat"
    with queue_mutex:
        broadcast_queue.put({"message": connect_message, "username": "Server"})

    # Loop to work with the client
    while True:
        try:
            # Receive the pickled message from the client and unpickle it
            data = client_socket.recv(1024)
            if not data:
                break

            message = pickle.loads(data)["message"]
            username = pickle.loads(data)["username"]

            # Put the message to the broadcast queue
            with queue_mutex:
                broadcast_queue.put({"message": message, "username": username})

        except Exception as e:
            print(f"Error working with client: {e}")
            break

    # Remove the client from the clients list
    with clients_mutex:
        clients.remove(client_socket)

    # Put client disconnect message to the broadcast queue
    print("Client disconnected:", client_socket.getpeername())
    leave_message = f"{client_name} has left the chat"
    with queue_mutex:
        broadcast_queue.put({"message": leave_message, "username": "Server"})

    client_socket.close()

def broadcast_messages():
    # Loop to broadcast the messages
    while True:
        try:
            # Get the message from the queue and broadcast it to all the clients
            message = broadcast_queue.get()

            with clients_mutex:
                for client_socket in clients:
                    client_socket.sendall(pickle.dumps(message))

        except Exception as e:
            print(f"Error broadcasting message: {e}")

def start_server():
    # Initialize the server socket, bind, and start listening for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))

    server_socket.listen(500)
    print(f"Server listening on {HOST}:{PORT}")

    # Start the broadcast thread
    broadcast_thread = threading.Thread(target=broadcast_messages)
    broadcast_thread.start()

    # Loop to accept clients connection without closing the server
    while True:
        try:
            # Accept the client's connection
            client_socket, client_address = server_socket.accept()
            print("New client connected:", client_address)

            # Add the client to the clients list and start a new thread to work with the client
            with clients_mutex:
                clients.append(client_socket)

            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

        except Exception as e:
            print(f"Error accepting client connection: {e}")

    server_socket.close()

start_server()
