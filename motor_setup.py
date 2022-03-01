import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os

# Occasionally, it can't connect to radius_board. Power cycling seems like a temporary fix, but I'm not sure what to do.
radius_board = odrive.find_any(serial_number="208F3388304B")
theta_board = odrive.find_any(serial_number="388937553437")

assert theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."
assert radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

theta_motor = ODrive_Ease_Lib.ODrive_Axis(theta_board.axis0, 10, 30)
r1 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis0, 20, 20)  # Blue tape #
r2 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis1, 20, 20)  # Orange tape

# Reboot ODrives until they are calibrated.
while not (r1.is_calibrated() and r2.is_calibrated()):
    radius_board.reboot()
while not theta_motor.is_calibrated():
    theta_board.reboot()
print("All motors are calibrated!")


# Mirror Mode: any direct command sent to r1 will also be set for r2.
r2.axis.controller.config.axis_to_mirror = 0
r2.axis.controller.config.input_mode = 7
r2.axis.requested_state = 8




def move(in_or_out):
    if in_or_out == "in":
        r1.set_relative_pos(25)
        r2.set_relative_pos(25)
    elif in_or_out == "out":
        r1.set_relative_pos(-25)
        r2.set_relative_pos(-25)




















# Shouldn't need these again
theta_motor.set_gains()
r1.set_gains()
r2.set_gains()

theta_motor.calibrate()

r1.calibrate_with_current_lim(40)
r2.calibrate_with_current_lim(40) # might need some more, not exactly sure how much to give

theta_motor.axis.motor.config.pre_calibrated = True
r1.axis.motor.config.pre_calibrated = True
r2.axis.motor.config.pre_calibrated = True
theta_motor.axis.config.startup_encoder_offset_calibration = True
r1.axis.config.startup_encoder_offset_calibration = True
r2.axis.config.startup_encoder_offset_calibration = True
radius_board.save_configuration()
theta_board.save_configuration()


