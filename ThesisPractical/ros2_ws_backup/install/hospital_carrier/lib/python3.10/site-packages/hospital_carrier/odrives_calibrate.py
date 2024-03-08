import odrive.enums
import time

from .odrive_axes_of import axes_of
from .odrive_errors import check_odrive_errors

def calibrate_odrives(odrv, recalibrate=False, calibrate_motors=False):
    # Unless told to calibrate_motors, we assume that the motors have already
    # been calibrated. We possibly only need to set up the encoders.
    def axis_is_ready(odrv):
        for axis in axes_of(odrv):
            with axis.lock:
                motor_is_ready = True
                if calibrate_motors:
                    motor_is_ready = axis.axis.motor.is_calibrated
                encoder_is_ready = axis.axis.encoder.is_ready
                #print("IS READY:", encoder_is_ready, motor_is_ready, encoder_is_ready)
                yield motor_is_ready and encoder_is_ready

    if all(axis_is_ready(odrv)) and not recalibrate:
        print('No calibration needed.')
        return
    
    print('Calibrating ODrives...')

    for axis in axes_of(odrv):
        with axis.lock:
            print("TYPE", type(axis), type(axis.axis))
            print("------------ CALIBRATION ------------")
            # Looks like this does not work over ASCII any more
            
            # this is readonly parameter
            #axis.axis.encoder.is_ready = False
            if calibrate_motors:
                axis.axis.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
            else:
                axis.axis.requested_state = odrive.enums.AXIS_STATE_ENCODER_OFFSET_CALIBRATION

            #axis.axis.read_line()
            #axis.axis.flush_state()
    
    # kui lugemist pole, siis veateade j'rgmise readi kohta
            
    while not all(axis_is_ready(odrv)):
         check_odrive_errors(odrv)
         time.sleep(0.1)

    print('Calibrated!')

    if calibrate_motors:
        print('Phase inductances:')
        for axis in axes_of(odrv):
            with axis.lock:
                print('{}: {:.10f}'.format(axis.id, axis.axis.motor.config.phase_inductance))

        print('Phase resistances:')
        for axis in axes_of(odrv):
            with axis.lock:
                print('{}: {:.10f}'.format(axis.id, axis.axis.motor.config.phase_resistance))
