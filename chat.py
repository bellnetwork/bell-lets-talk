import os
import tkinter as tk
import socketio

os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def message(data):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Server: " + data + "\n")
    chat_history.config(state=tk.DISABLED)

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")
    print(data)

@sio.event
def disconnect():
    print("I'm disconnected!")

def start_chat(event=None):  # Add event=None to handle callback from bind
    global username
    username = username_entry.get()
    if username:
        # Connect to the Socket.IO server
        try:
            sio.connect("http://ebxyb83tr3cbw.bellsocket.com", transports=['websocket'])
        except Exception as e:
            print("Connection Error:", e)
            return

        # Show chat window
        login_window.destroy()
        open_chat_window()

def open_chat_window():
    global chat_window, chat_history, entry
    chat_window = tk.Tk()
    chat_window.title("Chat - " + username)

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
    elif message.lower() == '/clear':
        chat_history.config(state=tk.NORMAL)
        chat_history.delete(1.0, tk.END)
        chat_history.config(state=tk.DISABLED)
    elif message:
        # Send the message to the server
        sio.emit('message', username + ": " + message)

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
