import serial
import re
import time

from .odrive_errors import ODriveUARTError

class UARTProxy():
    def __init__(self, serial, proxy_name=''):
        self.__dict__['serial'] = serial
        self.__dict__['proxy_name'] = proxy_name

        watchdog_cmd = None
        if proxy_name == 'axis0.':
            watchdog_cmd = 'u 0'
        elif proxy_name == 'axis1.':
            watchdog_cmd = 'u 1'
        if watchdog_cmd:
            self.__dict__['watchdog_feed'] = lambda: self.write_command(watchdog_cmd)

    @staticmethod
    def subproxy_names():
        yield 'config'
        for axis in ['axis0', 'axis1']:
            yield axis
            yield axis + '.config'
            yield axis + '.encoder'
            yield axis + '.encoder.config'
            yield axis + '.motor'
            yield axis + '.motor.config'
            yield axis + '.controller'
            yield axis + '.controller.config'
            yield axis + '.sensorless_estimator'
            yield axis + '.sensorless_estimator.config'
            yield axis + '.trap_traj'
            yield axis + '.trap_traj.config'

    def __getattr__(self, attr):
        attr_path = self.proxy_name + attr
        if attr_path in self.subproxy_names():
            return UARTProxy(self.serial, attr_path + '.')
        #self.get_logger().info('ATTR', attr)
        return self.read_parameter(attr_path)

    def __setattr__(self, attr, value):
        attr_path = self.proxy_name + attr
        self.write_parameter(attr_path, value)
    
    @staticmethod
    def gcode_csum(cmd):
        if len(cmd) == 1:
            return ord(cmd)
        cs = ord(cmd[0]) ^ ord(cmd[1])
        for c in cmd[2:]:
            cs = cs ^ ord(c)
        return cs
    
    @staticmethod
    def add_checksum(cmd):
        cmd = cmd + " "
        return cmd + "*" + str(UARTProxy.gcode_csum(cmd))

    def write_command(self, cmd):
        if len(cmd) >= 2:
            cmd = self.add_checksum(cmd)
        #self.get_logger().info('COMMAND', cmd, self.serial.port)
        cmd_formatted = '{}\n'.format(cmd)
        cmd_bytes = cmd_formatted.encode('ascii')
        #self.get_logger().info('UART write: {}'.format(cmd_bytes))
        self.serial.write(cmd_bytes)

    def read_line(self):
        line = self.serial.readline()
        return line.decode('ascii').rstrip()
    
    def flush_state(self):
        self.write_command('')
        self.read_line()

    @staticmethod
    def convert_parameter_to_its_type(param, orig_cmd):
        if len(param) == 0:
            raise ODriveUARTError('No response')
        if re.fullmatch('-?[0-9]+', param):
            return int(param)
        if re.fullmatch('-?[0-9]+\.[0-9]*', param):
            return float(param)
        # bug in odrive 0.5.2 where 0d is returned instead of False/0
        if param == "0d":
            return 0
        raise ODriveUARTError('Cannot read "{}" as an int or float for command {}'.format(param, orig_cmd))

    @staticmethod
    def convert_parameter_to_string(param):
        if isinstance(param, bool):
            return str(int(param))
        if isinstance(param, int):
            return str(param)
        if isinstance(param, float):
            return '{:.10f}'.format(param)
        raise ODriveUARTError('The type "{}" is not suitable for writing'.format(str(type(param))))
        
    @staticmethod
    def checksum_check(line):
        has_checksum = line.find("*")
        #self.get_logger().info("INTERM", line, has_checksum)
        if has_checksum < 0:
            return line
        splits = line.split("*", 1)
        checksum = UARTProxy.gcode_csum(splits[0])
        try:
            odrive_csum = int(splits[1])
        except:
            raise RuntimeWarning("Malformed checksum received from Odrive:", splits[1])
            return line
        if checksum == odrive_csum:
            return splits[0]
        raise RuntimeWarning("Checksum does not match:" + line + "Expected checksum:", checksum, splits[1])

    def read_parameter(self, param_path):
        cmd = 'r ' + param_path
        try:
            self.write_command(cmd)
            line = self.read_line()
        except UnicodeDecodeError as ex:
            raise RuntimeError("Unicode decoding failed: ", cmd, ex)
            
        line = self.checksum_check(line)
        #self.get_logger().info('RES', line)
        return self.convert_parameter_to_its_type(line, orig_cmd=cmd)

    def write_parameter(self, param_path, value):
        value_str = self.convert_parameter_to_string(value)
        cmd = 'w ' + param_path + ' ' + value_str
        #self.get_logger().info("WRITE", cmd)
        self.write_command(cmd)
        
    def save_configuration(self):
        self.write_command('ss')

    def reboot(self):
        self.write_command('sr')
        
    def persist_parameters(self):
        self.save_configuration()
        self.reboot()
        time.sleep(2)

class ODriveUART(UARTProxy):
    def __init__(self, port):
        ser = serial.Serial()
        ser.port = port
        #self.get_logger().info("MY PORT", port)
        ser.baudrate = 115200
        ser.timeout = 0.1 # read timeout
        ser.write_timeout = 0.1

        super().__init__(ser)

    def __enter__(self):
        self.serial.__enter__()
        self.flush_state()
        return self

    def __exit__(self, *args):
        return self.serial.__exit__(*args)
