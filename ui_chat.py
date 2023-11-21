# The ultimative bell let's talk ui

import os
import tkinter as tk
import socketio
import platform

# Import winsound if the platform is Windows
if platform.system() == "Windows":
    import winsound
    
os.environ['TK_SILENCE_DEPRECATION'] = '1'
version = "1.0.0"
# Create a Socket.IO client 
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to bell let's talk!")

@sio.event
def connect_error(data):
    print("The connection failed! Reconecting...")
    print(data)

@sio.event
def disconnect():
    print("I'm disconnected!")
    
def play_sound():
    if platform.system() == "Windows":
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    else:
        os.system('afplay /System/Library/Sounds/Glass.aiff')

@sio.event
def message(data):
    play_sound()
    chat_history.config(state=tk.NORMAL)
    if 'text' in data:
        chat_history.insert(tk.END, data['text'] + "\n")
    else:
        chat_history.insert(tk.END, str(data) + "\n")
    chat_history.config(state=tk.DISABLED)

chat_history = None  # Initialize as None globally

def start_chat(event=None):
    global username
    username = username_entry.get()
    if username:
        # Connect to the Socket.IO server with the username and version as query parameters
        connection_url = f"http://ebxyb83tr3cbw.bellsocket.com?username={username}&version={version}"
        try:
            sio.connect(connection_url, transports=['websocket'])
        except Exception as e:
            print("Connection Error:", e)
            return

def open_chat_window():
    global chat_window, chat_history, entry
    chat_window = tk.Tk()
    chat_window.title("Bell Let´s Talk - " + username)

    chat_frame = tk.Frame(chat_window, bg="white")
    scrollbar = tk.Scrollbar(chat_frame)
    chat_history = tk.Text(chat_frame, height=50, width=50, yscrollcommand=scrollbar.set, fg="white", bg="gray")
    scrollbar.config(command=chat_history.yview)
    chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_history.config(state=tk.DISABLED)
    chat_frame.pack(expand=True, fill=tk.BOTH)

    entry = tk.Entry(chat_window, width=40, fg="white", bg="darkblue")
    entry.pack(padx=10, pady=10)
    entry.bind("<Return>", send_message)  # Bind the Enter key to send_message

    send_button = tk.Button(chat_window, text="Send", command=lambda: send_message())
    send_button.pack(pady=10)

    chat_window.mainloop()

def send_message(event=None):
    message = entry.get()
    entry.delete(0, tk.END)

    if message.lower() == '/exit':
        chat_window.destroy()
        sio.disconnect()
        return
    elif message.lower() == '/users':
        # Send a user list request to the server
        sio.emit('get_users')
    elif message.lower().startswith('/pm '):
        parts = message.split(' ', 2)
        if len(parts) == 3:
            # Send private message to the server
            sio.emit('private_message', {'target_username': parts[1], 'message': parts[2]})
        else:
            chat_history.insert(tk.END, "Invalid private message format. Use: /pm <username> <message>\n")
    elif message.lower() == '/global':
        # Send a global switch message to the server
        sio.emit('switch_to_global', {'username': username})
    # Clear the chat history
    elif message.lower() == '/clear':
        chat_history.config(state=tk.NORMAL)
        chat_history.delete(1.0, tk.END)
        chat_history.config(state=tk.DISABLED)
    elif message.lower() == '/version' or message.lower() == '/v':
        chat_history.insert(tk.END, "Bell Let's Talk " + version + "\n")
    elif message.startswith('/'):
        chat_history.insert(tk.END, "Invalid command. Type /help to see the list of commands.\n")
    elif message.lower() == '/help' or message.lower() == '/h':
        chat_history.insert(tk.END, "Commands:\n")
        chat_history.insert(tk.END, "/exit - Exit the chat\n")
        chat_history.insert(tk.END, "/pm <username> <message> - Send a private message\n")
        chat_history.insert(tk.END, "/global - Switch to global chat\n")
        chat_history.insert(tk.END, "/clear - Clear the chat\n")
        chat_history.insert(tk.END, "/users - Show the list of users\n")
    elif message:
        # Send the message to the server
        sio.emit('message', username + ": " + message)

@sio.event
def user_list(data):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Online Users: " + ", ".join(data) + "\n")
    chat_history.config(state=tk.DISABLED)

# Login Window
login_window = tk.Tk()
login_window.title("Login")

username_label = tk.Label(login_window, text="Enter Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()
username_entry.bind("<Return>", start_chat)  # Bind Enter key to start_chat

start_chat_button = tk.Button(login_window, text="Start Chat", command=start_chat)
start_chat_button.pack()

login_window.mainloop()
