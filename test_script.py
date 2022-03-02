import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os

# STARTER CODE FOR PYTHON CONSOLE TESTING

# Occasionally, it can't connect to radius_board. Power cycling seems like a temporary fix, but I'm not sure what to do.
radius_board = odrive.find_any(serial_number="208F3388304B")
theta_board = odrive.find_any(serial_number="388937553437")

assert theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."
assert radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

radius_board.clear_errors()

theta_motor = ODrive_Ease_Lib.ODrive_Axis(theta_board.axis0, 10, 30)
r1 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis0, 20, 20)  # Blue tape #
r2 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis1, 20, 20)  # Orange tape

# Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
# are calibrated.
while not (r1.is_calibrated() and r2.is_calibrated()):
    print("r not calibrated")
    radius_board.reboot()
    time.sleep(10)
while not theta_motor.is_calibrated():
    print("theta not calibrated")
    theta_board.reboot()
    time.sleep(10)
print("All motors are calibrated!")


def home():
    r1.set_vel(-10)
    r2.set_vel(-10)

    while True:
        if r1.get_vel() > -0.05 and r2.get_vel() > -0.05:
            r1.set_vel(0)
            r1.set_home()

            r2.set_vel(0)
            r2.set_home()
            break


def move(in_or_out):
    if in_or_out == "in":
        r1.set_rel_pos_traj(25, 10, 15, 10)
        r2.set_rel_pos_traj(25, 10, 15, 10)
    elif in_or_out == "out":
        r1.set_rel_pos_traj(-25, 10, 15, 10)
        r2.set_rel_pos_traj(-25, 10, 15, 10)
    r2.wait()


move("in")

# in_or_out = "in"
# for i in range(5):
#     move(in_or_out)
#     # r1.set_rel_pos_traj(sign * 5, 10, 15, 10)
#     # r2.set_rel_pos_traj(sign * 5, 10, 15, 10)
#     in_or_out = "out" if in_or_out == "in" else "in"

home()

r1.idle()
r2.idle()

ODrive_Ease_Lib.dump_errors(radius_board)
