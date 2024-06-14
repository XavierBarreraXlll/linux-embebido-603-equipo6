import socket
import threading
from tkinter import *

# ========== Funciones del Cliente ==========

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 65432))
    listen_for_data(client)

def listen_for_data(client):
    while True:
        try:
            data = client.recv(1024)
            if data:
                humidity, temperature = data.decode('utf-8').split(',')
                print(f"Datos recibidos: Humedad={humidity}, Temperatura={temperature}")
                update_gui(humidity, temperature)
        except Exception as e:
            print(f"Error recibiendo datos del servidor: {e}")
            break

def update_gui(humidity, temperature):
    humidity_label['text'] = f"Humedad: {humidity}"
    temperature_label['text'] = f"Temperatura: {temperature}"

# ========== Código Principal del Cliente ==========

if __name__ == '__main__':
    root = Tk()
    root.title('Cliente TCP')
    root.geometry('400x200')

    # Crear un frame para el layout
    frame = Frame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Crear etiquetas para mostrar los datos
    temperature_label = Label(frame, text="Temperatura: --")
    humidity_label = Label(frame, text="Humedad: --")

    # Colocar los widgets en el frame usando grid.
    temperature_label.grid(row=0, column=0, padx=10, pady=10)
    humidity_label.grid(row=1, column=0, padx=10, pady=10)

    # Iniciar el cliente TCP en un hilo separado para no bloquear la GUI
    client_thread = threading.Thread(target=start_client)
    client_thread.daemon = True
    client_thread.start()

    root.mainloop()
