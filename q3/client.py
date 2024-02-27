# Name: Vladyslav Huziienko
# Student ID: 180749210
# Date: 27 Feb 2024

import socket
import threading
import pickle
import time

TKINTER_INSTALLED = True

# Check if Tkinter is installed
try:
    from tkinter import *
except:
    TKINTER_INSTALLED = False
    print("!!! IMPORTANT !!!! \nTkinter is not installed. Please install it to run the client as a desktop application. Withought Tkinter, the client will run as a console application.")

# Server's address and port
HOST = '127.0.0.1'
PORT = 9978

# Global variable to store the username
global username_gl
username_gl = ""

# Function to receive messages from the server and display them
def receive_messages(client_socket, chat_box):
    while True:
        try:
            # Receive the pickled message from the server and unpickle it
            message = client_socket.recv(1024)
            unpickled_message = pickle.loads(message)

            # Get the message and the username from the unpickled message
            text = unpickled_message.get("message")
            username = unpickled_message.get("username")

            # If Tkinter is installed, display the message in the chat box
            if TKINTER_INSTALLED:
                chat_box.config(state=NORMAL)
                chat_box.insert(END, f"{username} > {text}\n")
                chat_box.config(state=DISABLED)
            else:
                # If Tkinter is not installed, display the message in the console
                print(f"{username} > {text}")
            time.sleep(0.1)
        except Exception as e:
            print("Disconnected from the server. \nError:", e)
            break

# Function to send messages to the server
def send_messages(client_socket, input_field):
    # Get the message from the input field
    message = input_field.get()
    
    # If the message is empty, return
    if not message:
        return
    
    # Send the pickled message to the server
    client_socket.sendall(pickle.dumps({"message": message, "username": username_gl}))
    input_field.delete(0, END)

# Function to load the chat interface
def create_chat_interface(chat_box, input_field, send_button):
    chat_box.pack()
    input_field.pack()
    send_button.pack()

# Function to start the client
def start_client():
    # Initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # If Tkinter is installed, create the login and chat interface
    if TKINTER_INSTALLED:
        # Create the root window
        root = Tk()
        root.geometry("1000x900")

        # Create the chat interface, but don't pack it yet
        chat_box = Text(root, state=DISABLED)
        input_field = Entry(root)
        input_field.bind("<Return>", lambda event: send_messages(client_socket, input_field))
        send_button = Button(root, text="Send", command=lambda: send_messages(client_socket, input_field))

        # Function to handle user login
        def login(client_socket):
            # Get the username from the username field
            global username_gl
            username_gl = username_field.get()
            username_gl = username_gl.strip()
            # If the username is empty, display an error message
            if not username_gl:
                login_label.config(text="Username cannot be empty.")
                return
            # Send the username to the server
            client_socket.sendall(pickle.dumps(username_gl))

            # Hide the login interface and display the chat interface
            username_field.pack_forget()
            login_button.pack_forget()
            login_label.pack_forget()

            create_chat_interface(chat_box, input_field, send_button)

        # Display the login interface
        login_label = Label(root, text="Enter your username:")
        login_label.pack()

        username_field = Entry(root)
        username_field.pack()

        login_button = Button(root, text="Login", command=lambda: login(client_socket))
        login_button.pack()

        # Start the receive thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_box))
        receive_thread.start()

        # Function to close the client
        def on_close():
            client_socket.close()
            root.destroy()
            exit()

        # Bind the close event to the on_close function
        root.protocol("WM_DELETE_WINDOW", on_close)
        
        # Start the main loop
        root.mainloop()
    else:
        # If Tkinter is not installed, run the client as a console application
        # Get the username from the user
        username = input("Enter your username: ")
        client_socket.sendall(pickle.dumps(username))

        # Start the receive thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, None))
        receive_thread.start()

        time.sleep(0.5)
        while True:
            # Get the message from the user and send it to the server
            message = input("> ")
            client_socket.sendall(pickle.dumps({"message": message, "username": username}))

# Start the client
if __name__ == '__main__':
    start_client()
