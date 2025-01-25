import socket
import threading
import pyperclip
import time

PORT = 8787
BUFFER_SIZE = 1024

PEER_IP = ""
PEER_PORT = PORT
IsRecieved = False

# Function to input the peer ip and port
def peer_input():
    global PEER_IP
    global PEER_PORT
    PEER_IP = input("Other device ip: ")
    print(f"Other device ip: {PEER_IP}")
    PEER_PORT = int(input("Input the other device port (default 8787): ") or PORT)

# Function to input the local port
def local_input():
    global PORT
    PORT = int(input("Input the local port (default 8787): ") or PORT)

# Function to receive the clipboard data from the other device
def server_thread(host="0.0.0.0", port=PORT):
    global IsRecieved
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if data:
            print(f"Received: {data}")
            pyperclip.copy(data)
            IsRecieved = True
            print("Clipboard updated!")

        conn.close()

# Function to send the clipboard data to the other device
def client_thread(peer_ip, peer_port):
    global IsRecieved
    last_clipboard = pyperclip.paste()
    while True:
        time.sleep(0.5)
        current_clipboard = pyperclip.paste()

        if current_clipboard != last_clipboard and IsRecieved == False:
            last_clipboard = current_clipboard
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((peer_ip, peer_port))
                client_socket.sendall(current_clipboard.encode('utf-8'))
                client_socket.close()
                print(f"Sended: {current_clipboard}")
            except Exception as e:
                print(f"Error while sending: {e}")
        elif IsRecieved == True:
            last_clipboard = current_clipboard
            IsRecieved = False

# Starts the server and the client in separeted threads
if __name__ == "__main__":
    peer_input()
    local_input()
    threading.Thread(target=server_thread, daemon=True).start()
    client_thread(PEER_IP, PEER_PORT)
