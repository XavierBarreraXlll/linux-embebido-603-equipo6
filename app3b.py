from tkinter import *
from tkinter import Tk
from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Button
from PIL import Image, ImageTk  # Importing PIL for image handling

# Seriales
from sensor_serial import BAUDRATES
from sensor_serial import SensorSerial
from utils import find_available_serial_ports

# Assets
back = "/home/equipo3/proyecto_final/Assets/Beige.png"
texture = "/home/equipo3/proyecto_final/Assets/Wood.png"
#button_sound = "/home/equipo3/proyecto_final/Assets/CHIME_FX_popper_01.wav"
icon_path = "/home/equipo3/proyecto_final/Assets/icon.ico"
    
# ========== Funciones Importantes de los Elementos ==========
    
def refresh_serial_devices():
    ports = find_available_serial_ports()
    serial_devices_combobox.selection_clear()
    serial_devices_combobox['values'] = ports
    
def create_sensor_serial()->SensorSerial:
    port = serial_devices_combobox.get()
    baudrate = baudrate_combobox.get()
    if port == '' or baudrate == 'Baudrate':
        raise ValueError(f'Incorrect values for {port=} {baudrate=}')
    sensor_serial = SensorSerial(
        port=port,
        baudrate=int(baudrate)
    )
    
def read_temperature() -> None:
    if sensor_serial is not None:
        temperature = sensor_serial.send('TC2')
        temperature_label['text'] = temperature[:-3]
        return
    raise RuntimeError("Serial connection has not been initialized")

# ========== Codigo Main ==========
    
if __name__ == '__main__':
    root = Tk()
    root.title('Detector de Puertos')
    root.iconbitmap(icon_path)
    root.geometry('700x280')
    ports = find_available_serial_ports() # Encuentra los puertos disponibles.
    
    # Load the background image
    image_path = back
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    
    # Load button images
    refresh_serial_devices_button_img = Image.open(texture).resize((170, 20))
    refresh_serial_devices_button_photo = ImageTk.PhotoImage(refresh_serial_devices_button_img)
    connect_serial_button_img = Image.open(texture).resize((80, 20))
    connect_serial_button_photo = ImageTk.PhotoImage(connect_serial_button_img)
    
    # Create a canvas.
    canvas = Canvas(root, width=image.width, height=image.height)
    canvas.pack(fill="both", expand=True)

    # Set the background image.
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Function to create and place labels and entries on the canvas.
    def create_widget(widget, row, column, padx=0, pady=0):
        canvas.create_window((column*100)+50, (row*30)+50, anchor="nw", window=widget)
        
    # Create buttons and comboboxes with images and text.
    serial_devices_combobox = Combobox(root, values=ports)
    refresh_serial_devices_button = Button(root, image=refresh_serial_devices_button_photo, text="Refresh Available Serial Devices", compound="center", fg="white", command=lambda: [refresh_serial_devices()], borderwidth=0)
    baudrate_combobox = Combobox(root,  values=['Baudrate'] + BAUDRATES)
    connect_serial_button = Button(root, image=connect_serial_button_photo, text="Connect Serial", compound="center", fg="white", command=lambda: [create_sensor_serial()], borderwidth=0)
    
    create_widget(serial_devices_combobox, 0, 0)
    create_widget(refresh_serial_devices_button, 0, 1.5)
    create_widget(baudrate_combobox, 0, 3.3)
    create_widget(connect_serial_button, 0, 4.8)
    
    root.mainloop()
