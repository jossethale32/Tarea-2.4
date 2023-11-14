import socket
import threading

# Dirección y puerto del servidor
HOST = '127.0.0.1'
PORT = 55556  # Cambiar a un puerto diferente

# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
try:
    client_socket.connect((HOST, PORT))
except socket.error:
    print("Servidor no responde. Desconectando.")
    exit()
# Solicitar al usuario que ingrese un nombre o identificación única
client_name = input("Ingresa tu nombre o identificación única: ")

if client_name.isalpha() or client_name.isdigit():
    # Función para recibir mensajes del servidor
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
            except socket.error:
                print("Error al recibir mensajes. Desconectando.")
                client_socket.close()
                break

    # Iniciar un hilo para recibir mensajes del servidor
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Enviar mensajes al servidor
    while True:
        try:
            message = input()
            full_message = f"{client_name}: {message}"
            client_socket.send(full_message.encode('utf-8'))
        except KeyboardInterrupt:
            exit()
        # Si el usuario escribe "adios", cerrar el cliente
        if message.lower() == "adios":
            break

    # Cerrar el socket después de salir del bucle
    client_socket.close()
else:
    print("Valor ingresado no valido!")
    client_socket.close()