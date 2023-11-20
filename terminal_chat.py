# The ultimative bell let's talk terminal

import os
import socketio
import threading

os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def message(data):
    print("\n" + data)

@sio.event
def connect():
    print("Connected to the chat server!")

@sio.event
def connect_error(data):
    print("The connection failed:", data)

@sio.event
def disconnect():
    print("Disconnected from the chat server")

def start_chat():
    global username
    username = input("Enter your username: ")
    if username:
        # Connect to the Socket.IO server
        try:
            # Include the username in the connection URL
            connection_url = f"http://ebxyb83tr3cbw.bellsocket.com?username={username}"
            sio.connect(connection_url, transports=['websocket'])
        except Exception as e:
            print("Connection Error:", e)
            return

        # Start the chat interface
        open_chat_interface()

def open_chat_interface():
    print(f"Welcome to the chat, {username}! Type '/exit' to leave.")
    while True:
        message = input("Your message: ")
        sio.emit('user_typing', {'typing': False}) # Notify server user stopped typing
        if message.lower() == '/exit':
            break
        elif message.lower().startswith('/pm '):
            parts = message.split(' ', 2)
            if len(parts) == 3:
                # Send private message to the server
                sio.emit('private_message', {'target_username': parts[1], 'message': parts[2]})
            else:
                print("Invalid private message format. Use: /private <username> <message>")
        elif message.lower() == '/global':
            # Send a global switch message to the server
            sio.emit('switch_to_global', {'username': username})
        elif message.lower() == '/clear':
            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')
        elif message:
            # Notify server user is typing
            sio.emit('user_typing', {'typing': True})
            # Send the message to the server
            sio.emit('message', username + ": " + message)
            sio.emit('user_typing', {'typing': False})  # Notify server user stopped typing

    sio.disconnect()

@sio.event
def user_typing_update(data):
    if data['typing']:
        print(f"\n{data['username']} is typing...")
    else:
        print(f"\n{data['username']} stopped typing.")
           
if __name__ == "__main__":
    start_chat()
