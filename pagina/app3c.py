import serial
from tkinter import *
from tkinter.ttk import Combobox
from sensor_serial import BAUDRATES, SensorSerial
from utils import find_available_serial_ports

# ========== Funciones Importantes de los Elementos ==========

def refresh_serial_devices():
    ports = find_available_serial_ports()
    serial_devices_combobox['values'] = ports

def create_sensor_serial():
    port = serial_devices_combobox.get()
    baudrate = baudrate_combobox.get()
    if port == '' or baudrate == 'Baudrate':
        raise ValueError(f'Incorrect values for {port=} {baudrate=}')
    global ser
    ser = serial.Serial(port, int(baudrate))
    ser.flushInput()
    read_serial_data()

def read_serial_data():
    try:
        if ser.in_waiting > 0:
            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            print(f"Received: {line}")  # Imprime el valor recibido para depuración
            
            # Dividir la línea recibida en humedad y temperatura
            if "Humedad:" in line and "Temperatura:" in line:
                parts = line.split('\t')
                humidity_part = parts[0].split(': ')[1]
                temperature_part = parts[1].split(': ')[1]

                temperature_label['text'] = f"Temperatura: {temperature_part}"
                humidity_label['text'] = f"Humedad: {humidity_part}"

        root.after(1000, read_serial_data)
    except Exception as e:
        print(f"Error reading serial data: {e}")

# ========== Codigo Main ==========

if __name__ == '__main__':
    root = Tk()
    root.title('Equipo 6')
    root.geometry('400x200')
    ports = find_available_serial_ports()  # Encuentra los puertos disponibles.

    # Create a frame for layout
    frame = Frame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Create buttons and comboboxes with text.
    serial_devices_combobox = Combobox(frame, values=ports)
    refresh_serial_devices_button = Button(frame, text="Refresh Available Serial Devices", command=refresh_serial_devices)
    baudrate_combobox = Combobox(frame, values=['Baudrate'] + BAUDRATES)
    connect_serial_button = Button(frame, text="Connect Serial", command=create_sensor_serial)
    temperature_label = Label(frame, text="Temperatura: --")
    humidity_label = Label(frame, text="Humedad: --")

    # Place the widgets on the frame using grid.
    serial_devices_combobox.grid(row=0, column=0, padx=10, pady=10)
    refresh_serial_devices_button.grid(row=0, column=1, padx=10, pady=10)
    baudrate_combobox.grid(row=1, column=0, padx=10, pady=10)
    connect_serial_button.grid(row=1, column=1, padx=10, pady=10)
    temperature_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    humidity_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()
