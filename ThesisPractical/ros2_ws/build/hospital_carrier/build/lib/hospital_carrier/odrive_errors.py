import rclpy
from rclpy.parameter import Parameter

import odrive.utils
import odrive.enums

from .odrive_axes_of import axes_of

v_needed = 34.0

class ODriveAxisError(Exception):
    pass

class ODriveVoltageTooLow(Exception):
    pass

class ODriveUARTError(Exception):
    pass

def check_odrive_errors(odrv):
    for o in odrv:
        with o.lock:
            v_measured = o.odrv.vbus_voltage
        if v_measured < v_needed:
            print('Battery voltage too low: {:.02f} V (we need at least {:.02f} V)!'.format(v_measured, v_needed))
            raise ODriveVoltageTooLow()

    def axis_errors(odrv):
        for axis in axes_of(odrv):
            with axis.lock:
                yield axis.axis.error

    if any(error != 0 for error in axis_errors(odrv)):
        print('Error at an axis!')

        for o in odrv:
            print('ODrive {}:'.format(o.id))
            if o.connection_type == 'usb':
                with o.lock:
                    odrive.utils.dump_errors(o.odrv)
                print()
            elif o.connection_type == 'uart':
                for axis in ['axis0', 'axis1']:
                    def print_error(path, errors_enum = None):
                        full_path = axis + '.' + path
                        with o.lock:
                            error_code = eval('o.odrv.' + full_path)
                        explanation = []
                        if errors_enum:
                            for name, value in errors_enum.__dict__.items():
                                if not name.startswith('__') and (value & error_code) != 0:
                                    explanation.append(name)
                        print('{} = {} ({})'.format(full_path, error_code, ' | '.join(explanation)))

                    print_error('motor.error', odrive.enums.MotorError)
                    print_error('encoder.error', odrive.enums.EncoderError)
                    print_error('sensorless_estimator.error')
                    print_error('error', odrive.enums.AxisError)
                    print()

        raise ODriveAxisError()

def clear_odrive_errors(odrv):
    print("Clearing all axes' errors...")
    for axis in axes_of(odrv):
        with axis.lock:
            axis.axis.error = 0
