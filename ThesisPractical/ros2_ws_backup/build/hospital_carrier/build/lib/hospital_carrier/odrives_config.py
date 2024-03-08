import odrive.enums

from .odrive_axes_of import axes_of
import time

def config_odrives(odrv):
    print('Configuring ODrives...')
    
    for o in odrv:
        with o.lock:
            if o.odrv.config.uart0_protocol != odrive.enums.STREAM_PROTOCOL_TYPE_ASCII_AND_STDOUT:
                # as of 0.5.2 the code will not even run when we have different protocal, but it may change in the future
                print("WARNING! WRONG PROTOCOL. ROBOT MAY NOT START. Set from odrivetool to STREAM_PROTOCOL_TYPE_ASCII_AND_STDOUT")
            
            o.odrv.config.enable_brake_resistor = False
            o.odrv.config.brake_resistance = 0.0 # full regenerative braking
            o.odrv.config.dc_max_negative_current = -30 # same as config.current_lim as we have no brake resistor
            o.odrv.persist_parameters()
                
    bandwidth = 5 # Hz; TODO measure

    for axis in axes_of(odrv):
        a = axis.axis
        with axis.lock:
            # not implemented in ASCII protocol
            a.motor.config.motor_type = odrive.enums.MOTOR_TYPE_HIGH_CURRENT
            a.motor.config.current_lim = 30
            a.motor.config.calibration_current = 10
            a.motor.config.pole_pairs = 2
            a.motor.config.requested_current_range = 60
            a.persist_parameters()

            #if axis.id in [('/dev/ttyAMA1', 1), (35576160596046, 1)]:
            if axis.id in [('/dev/ttyAMA1', 1), (35705026399565, 1)]: # 2079396A4D4D
                a.motor.config.phase_inductance = 0.0001570000
                a.motor.config.phase_resistance = 0.1551430000
            else:
                a.motor.config.phase_inductance = 0.0005079241818748415
                a.motor.config.phase_resistance = 0.22080011665821075

            a.motor.config.pre_calibrated = True
            
            # if this is set, current_lim fails >D
            a.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL

            cpr = 4 * 2048
            torque_const = 0.063
            a.motor.config.torque_constant = torque_const
            a.encoder.config.cpr = cpr

            a.encoder.config.bandwidth = 2000

            a.controller.config.pos_gain = 30   #96.53617858886719
            vel_gain = 0.09  #0.0001250000059371814 * torque_const * cpr
            a.controller.config.vel_gain = vel_gain
            a.controller.config.vel_integrator_gain = 0.45  #0.5 * bandwidth * vel_gain * torque_const * cpr
            a.controller.config.vel_limit = 200000.0 / cpr
            a.controller.config.vel_limit_tolerance = 1.2000000476837158
            a.controller.config.vel_ramp_rate = 10000.0 / cpr
            # removed, but undocumented
            #a.controller.config.setpoints_in_cpr = False

            a.config.watchdog_timeout = 0.8 # Must be significantly longer than the interval in watchdog.py
            a.persist_parameters()