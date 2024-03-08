import threading
import odrive
import serial

from .odrive_uart import ODriveUART

class ODriveConnection():
    odrive_locks = dict()

    def __init__(self, connection_type, serial_number_or_port):
        if connection_type not in ['usb', 'uart']:
            raise Exception('Invalid connection type "{}"', connection_type)
        self.connection_type = connection_type

        self.id = serial_number_or_port

        locks = self.__class__.odrive_locks
        if self.id in locks:
            self.lock = locks[self.id]
        else:
            self.lock = threading.Lock()
            locks[self.id] = self.lock

        self.odrv = None

    def create_conn(self):
        if self.connection_type == 'usb':
            serial_hex = format(self.id, 'X')
            with self.lock:
                self.odrv = odrive.find_any(serial_number=serial_hex)
        elif self.connection_type == 'uart':
            with self.lock:
                try:
                    self.odrv = ODriveUART(self.id).__enter__()
                except serial.SerialException:
                    self.get_logger().info("Odrive UART connection {} not established.".format(self.id))
                    self.odrv = None

        return self

    def stop_conn(self, *args):
        if self.odrv:
            if self.connection_type == 'uart':
                self.odrv.__exit__(*args)
            del self.odrv
        self.odrv = None
