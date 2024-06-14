import time
import serial

BAUDRATES = [
    9600,
    19200,
    38400,
    57600,
    115200,
]

class SensorSerial:

    def _init_(self, serial_port:str,
                baudrate:int = 115200,
                timeout:float = 2.0,
                connection_time:float = 3.0,
                reception_time:float = 0.5
        ) -> None:
        self.serial_connection = serial.Serial(
            port = serial_port,
            timeout = timeout,
            baudrate = baudrate,
        )
        self.connection_time = connection_time
        self.reception_time = reception_time
        time.sleep(self.connection_time)

    def send(self, to_send:str)->None:
        self.serial_connection.write(to_send.encode('utf-8'))
        time.sleep(self.reception_time)
        received = self.serial_connection.readline()
        return received

    def receive(self, ) ->None:
        received = self.serial_connection.readline()
        return received

    def close(self):
        self.serial_connection.close()

    def _del_(self):
        self.close()

    def _str_(self) -> str:
        return f"SerialSensor({self.serial_connection}, {self.connection_time=}, {self.reception_time=})"

    def _repr_(self) -> str:
        pass
    
    
# from arduserial.sensor_serial import SensorSerial
# arduino = SensorSerial('/dev/tty.usbmodem1101')
# arduino.send('soy Grant')