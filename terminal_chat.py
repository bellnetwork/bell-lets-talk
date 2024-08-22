# The ultimative bell let's talk terminal

import os
import socketio
import threading

os.environ['TK_SILENCE_DEPRECATION'] = '1'
version = "1.0.0"
sio = socketio.Client()
username = None

@sio.event
def message(data):
    if 'text' in data:
        print("\n" + data['text'])
    else:
        print("\n" + str(data))

@sio.event
def connect():
    print("Connected to bell let's talk!")
    chat_thread = threading.Thread(target=open_chat_interface)
    chat_thread.start()  # Start the chat interface in a separate thread

@sio.event
def connect_error(data):
    print("The connection failed! Reconnecting...")

@sio.event
def error(data):
    print("Error:", data['text'])

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
            connection_url = f"wss://ebxyb83tr3cbw.belldns.com?username={username}&version={version}"
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
        elif message.lower() == '/users':
            sio.emit('get_users')
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
        elif message.lower() == '/version' or message.lower() == '/v':
            print(f"Version: {version}")
        elif message.startswith('/'):
            print("Command not recognized. Type /h for help.")
        elif message.lower() == '/help' or message.lower() == '/h':
            print("\nCommands:")
            print("/exit - Leave the chat")
            print("/users - List online users")
            print("/pm <username> <message> - Send a private message to a user")
            print("/global - Switch to global chat")
            print("/clear - Clear the terminal")
        elif message:
            # Notify server user is typing
            sio.emit('user_typing', {'typing': True})
            # Send the message to the server
            sio.emit('message', username + ": " + message)
            sio.emit('user_typing', {'typing': False})  # Notify server user stopped typing

    sio.disconnect()

@sio.event
def user_list(data):
    print("\nOnline Users: " + ", ".join(data))

@sio.event
def user_typing_update(data):
    if data['typing']:
        print(f"\n{data['username']} is typing...")
    else:
        print(f"\n{data['username']} stopped typing.")
           
if __name__ == "__main__":
    start_chat()
