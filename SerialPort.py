import serial

class SerialPort:
    def __init__(self, comport:str, baudrate:int=9600, timeout:int=1):
        self.port_name = comport
        self.serial_port = serial.Serial(
            port = comport,
            baudrate=baudrate,
            timeout=timeout
        )
        self.serial_port.write_timeout = timeout

    def read_port(self):
        print("Reading from the serial port {}".format(self.port_name))
        while not self.serial_port.in_waiting: pass
        data = self.serial_port.read_until().decode('ascii')
        print("Data Received: {}".format(data))
        return data


    def write_port(self, data:str):
        try:
            data = data.encode('utf-8')
            n_bytes = self.serial_port.write(data)
            print("Number of Bytes written: {}".format(n_bytes))
        except serial.SerialTimeoutException as e: print("Caught {e}".format(e))
