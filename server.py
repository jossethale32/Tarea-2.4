import socket
import threading
import asyncio
import sys

# verificar o validaar argumento
args = len(sys.argv) - 1
verbose=0
if args>0:
    if '-v' in str(sys.argv[1]):
        verbose=1
else:
    verbose=0

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 55556

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace del socket al host y puerto
try:
    server_socket.bind((HOST, PORT))
except socket.error:
    print("Servidor no puede iniciarse")
    exit()
except Exception:
    print("Servidor no puede iniciarse")
    exit()
# Escuchar conexiones entrantes
server_socket.listen()

# Lista para almacenar las conexiones de los clientes
clients = []

# Función para enviar mensajes de difusión a todos los clientes
def broadcast(message, sender_socket=None):
    encoded_message = message.encode('utf-8')  # Codificar el mensaje a bytes
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(encoded_message)
            except socket.error:
                clients.remove(client_socket)

# Función para manejar la conexión con cada cliente
def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            message2 = (message.decode('utf-8')).split('-')                                 #parsear variaable con ip publica oculta antes de hacer split
            if verbose == 1:                                                                #use -v for verbose output and use variable = 1
                print(f"{client_address} - {message2[0]} {message2[1]}")
            if message2[1].lower() == "adios":
                # Enviar mensaje de despedida a los demás clientes
                broadcast(f"{client_address} se ha desconectado.", client_socket)
                # Cerrar el socket del cliente
                clients.remove(client_socket)
                break
            broadcast(f"[{client_address}] {message2[1]}", client_socket)
        except socket.error:
            clients.remove(client_socket)
            break

# Metodo de Difusion de mensajes desde el servidor
def difusion():
    if len(clients) > 0:
        try:
            re=input("")
            if len(re) > 0:
                for cliente in clients:
                    try:
                        cliente.send(str(re).encode('utf-8'))
                    except:
                        clients.remove(cliente)
        except Exception:
            print ("Sesion Terminada.")
            exit()

async def main():
    # Ciclo principal para aceptar conexiones de clientes
    while True:
        # Aceptar una nueva conexión
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")
        await asyncio.sleep(1)
        # Agregar el socket del cliente a la lista
        clients.append(client_socket)

        # Iniciar un hilo para manejar la conexión con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

        # Iniciar un hilo para despues que cada cliente se conecte para envio de mensajes en difucion a todos ellos
        difusiont = threading.Thread(target=difusion)
        difusiont.start()


asyncio.run(main())