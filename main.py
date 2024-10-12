import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Para la barra de progreso
from PIL import Image, ImageTk  # Para manejar la imagen
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time  # Para manejar el tiempo
import webbrowser  # Para abrir Google Maps en el navegador

# Variables globales
data_values = []  # Para almacenar los datos del marcapasos (tensión)
time_values = []  # Para almacenar el tiempo de recepción
client_socket = None  # Socket para la conexión
pacemaker_location = None  # Variable para almacenar la ubicación del marcapasos

# Función para simular una pantalla de carga con barra de progreso
def loading_screen():
    progress_window = tk.Toplevel(root)
    progress_window.title("Cargando...")

    # Texto para la pantalla de carga
    loading_label = tk.Label(progress_window, text="Cargando, por favor espera...")
    loading_label.pack(pady=20)

    # Barra de progreso
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    # Función que actualiza la barra de progreso
    def update_progress(value=0):
        progress_bar['value'] = value
        if value < 100:
            root.after(100, update_progress, value + 10)  # Incrementa el progreso cada 100 ms
        else:
            progress_window.destroy()  # Cierra la pantalla de carga al completar
            connect_to_pacemaker()  # Llama a la función de conexión

    update_progress()  # Inicia la actualización de la barra

# Función para conectarse al marcapasos
def connect_to_pacemaker():
    global client_socket
    ip_address = 'localhost'  # IP del marcapasos
    port = 25565  # Puerto del marcapasos

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        messagebox.showinfo("Conexión", "Conexión exitosa al marcapasos")

        # Mostrar la IP en la etiqueta
        ip_label.config(text=f"IP del Marcapasos: {ip_address}")

        receive_data()  # Llama a la función para recibir datos

    except socket.error as e:
        messagebox.showerror("Error", f"No se pudo conectar: {e}")

# Función para recibir datos del marcapasos
def receive_data():
    global data_values, time_values, pacemaker_location
    try:
        data = client_socket.recv(1024)
        if data:
            # Supongamos que el dato es un string en el formato "tensión,latitud,longitud"
            received_data = data.decode('utf-8').split(',')
            tension_value = float(received_data[0])  # Tensión
            latitude = float(received_data[1])  # Latitud
            longitude = float(received_data[2])  # Longitud

            data_values.append(tension_value)
            current_time = time.time()  # Obtener el tiempo actual
            time_values.append(current_time - time_values[0] if time_values else 0)  # Calcular el tiempo transcurrido
            
            data_label.config(text=f"Tensión: {tension_value}")

            # Guardar la ubicación del marcapasos
            pacemaker_location = (latitude, longitude)

            # Actualizar la gráfica
            plot_data()

        root.after(3000, receive_data)  # Actualiza cada 3 segundos
    except Exception as e:
        messagebox.showerror("Error", f"Error al recibir datos: {e}")

# Función para actualizar la gráfica
def plot_data():
    ax.clear()  # Limpiar los ejes antes de dibujar de nuevo
    ax.plot(time_values, data_values, marker='o')  # Graficar los datos
    ax.set_title("Tensión del Marcapasos vs Tiempo")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Tensión (mmHg)")  # Añadir la unidad si es relevante
    if data_values:  # Evitar error si la lista está vacía
        ax.set_ylim(min(data_values) - 5, max(data_values) + 5)  # Ajustar los límites de Y
        ax.set_xlim(0, max(time_values) if time_values else 1)  # Ajustar límites de X
    plt.xticks(rotation=45)  # Rotar etiquetas del eje X si es necesario
    plt.tight_layout()  # Ajustar el diseño
    canvas.draw()  # Actualizar la gráfica

# Función para refrescar los datos
def refresh_data():
    global data_values, time_values
    data_values.clear()  # Limpiar datos antiguos
    time_values.clear()  # Limpiar tiempos antiguos
    data_label.config(text="Tensión: Esperando...")
    plot_data()  # Actualizar la gráfica

# Función para abrir Google Maps con la ubicación del marcapasos
def open_map():
    if pacemaker_location:
        lat, lon = pacemaker_location
        url = f"https://www.google.com/maps?q={lat},{lon}"  # Crear la URL de Google Maps
        webbrowser.open(url)  # Abrir la URL en el navegador predeterminado
    else:
        messagebox.showwarning("Ubicación no disponible", "No se ha recibido la ubicación del marcapasos.")

# Crear la ventana principal de la GUI
root = tk.Tk()
root.title("Heart Beat")

# Cargar el logo desde la misma carpeta que el script
logo_image = Image.open("F:\Repositorys\My Projects\Actualizaciones\0.1\Heart_Beat-app\image.png")  # Asegúrate de que la imagen esté en la misma carpeta
logo_image = logo_image.resize((75, 75))  # Redimensionar si es necesario
logo_photo = ImageTk.PhotoImage(logo_image)

# Mostrar el logo en la ventana
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=10)

# Etiqueta para mostrar datos del marcapasos
data_label = tk.Label(root, text="Esperando datos...")
data_label.pack(pady=20)

# Etiqueta para mostrar la IP del marcapasos
ip_label = tk.Label(root, text="IP del Marcapasos: Desconocida")
ip_label.pack(pady=20)

# Crear figura y ejes para la gráfica
fig, ax = plt.subplots(figsize=(6, 4))  # Cambiar el tamaño de la figura a más razonable
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=20)

# Marco para contener los botones
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Botón para conectar al marcapasos, con la pantalla de carga previa
connect_button = tk.Button(button_frame, text="Iniciar", command=loading_screen)
connect_button.pack(side=tk.LEFT, padx=10)

# Botón para refrescar datos
refresh_button = tk.Button(button_frame, text="Refrescar Datos", command=refresh_data)
refresh_button.pack(side=tk.LEFT, padx=10)

# Botón para abrir Google Maps
map_button = tk.Button(button_frame, text="Ver en Google Maps", command=open_map)
map_button.pack(side=tk.RIGHT, padx=10)

# Iniciar la GUI
root.mainloop()

# Crear figura y ejes para la gráfica
fig, ax = plt.subplots(figsize=(6, 4))  # Cambiar el tamaño de la figura a más razonable
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=20)

# Marco para contener los botones
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# Botón para conectar al marcapasos, con la pantalla de carga previa
connect_button = tk.Button(button_frame, text="Iniciar", command=loading_screen)
connect_button.pack(side=tk.LEFT, padx=10)

# Botón para refrescar datos
refresh_button = tk.Button(button_frame, text="Refrescar Datos", command=refresh_data)
refresh_button.pack(side=tk.LEFT, padx=10)

def verificar_pulso(pulso, edad):
    # Definir los rangos normales de pulso por edad
    rangos_normales = {
        '0-1': (100, 160),
        '1-4': (80, 120),
        '5-10': (70, 110),
        '11-17': (60, 100),
        '18-64': (60, 100),
        '65+': (50, 100)
    }

    # Determinar el rango de edad
    if edad <= 1:
        rango = rangos_normales['0-1']
    elif edad <= 4:
        rango = rangos_normales['1-4']
    elif edad <= 10:
        rango = rangos_normales['5-10']
    elif edad <= 17:
        rango = rangos_normales['11-17']
    elif edad <= 64:
        rango = rangos_normales['18-64']
    else:
        rango = rangos_normales['65+']

    # Verificar el pulso
    if pulso < rango[0]:
        print("¡Advertencia! El pulso es demasiado bajo.")
    elif pulso > rango[1]:
        print("¡Advertencia! El pulso es demasiado alto.")
    else:
        print("El pulso está dentro de los niveles normales.")

# Ejemplo de uso
verificar_pulso(55, 30)  # Pulsaciones bajas
verificar_pulso(75, 30)  # Pulsaciones normales
verificar_pulso(110, 30)  # Pulsaciones altas

# Botón para abrir Google Maps
map_button = tk.Button(button_frame, text="Ver en Google Maps", command=open_map)
map_button.pack(side=tk.RIGHT, padx=10)

# Iniciar la GUI
root.mainloop()
