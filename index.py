import socket

# Definir la dirección IP y el puerto del emulador
ip_address = 'localhost'  # Usar localhost para la conexión local
port = 25565  # Asegúrate de que coincida con el puerto del emulador

# Crear el socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al emulador
try:
    client_socket.connect((ip_address, port))
    print("Conexión establecida con el emulador")

    # Recibir datos
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Datos recibidos: {data.decode('utf-8')}")
except socket.error as e:
    print(f"Error de conexión: {e}")
finally:
    client_socket.close()

