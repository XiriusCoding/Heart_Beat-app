import socket

# Definir la dirección IP y el puerto del dispositivo marcapasos
ip_address = '192.168.1.100'  # Reemplaza con la IP del marcapasos
port = 12345  # Reemplaza con el puerto correcto

# Crear el socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al marcapasos
try:
    client_socket.connect((ip_address, port))
    print("Conexión establecida con el marcapasos")

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
