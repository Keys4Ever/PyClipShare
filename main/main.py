import socket
import threading
import pyperclip
import time

PORT = 8787
BUFFER_SIZE = 1024

PEER_IP = "192.168.1.2" 
PEER_PORT = PORT
IsRecieved = False

def peer_ip_input():
    global PEER_IP
    PEER_IP = input("Ingrese la IP del otro dispositivo: ")
    print(f"IP del otro dispositivo: {PEER_IP}")


# Función para ejecutar el servidor y recibir datos
def server_thread(host="0.0.0.0", port=PORT):
    global IsRecieved
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión entrante desde {addr}")

        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if data:
            print(f"Recibido: {data}")
            pyperclip.copy(data)
            IsRecieved = True
            print("Clipboard actualizado!")

        conn.close()

# Función para enviar datos al otro dispositivo
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
                print(f"Enviado: {current_clipboard}")
            except Exception as e:
                print(f"Error al enviar: {e}")
        elif IsRecieved == True:
            last_clipboard = current_clipboard
            IsRecieved = False

# Inicia el servidor y el cliente en threads separados
if __name__ == "__main__":
    peer_ip_input()
    threading.Thread(target=server_thread, daemon=True).start()
    client_thread(PEER_IP, PEER_PORT)
