import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os


class ConferenceSandTable:
    def __init__(self):
        # Occasionally, it can't connect to radius_board. Power cycling seems like a temporary fix, but I'm not sure
        # what to do.

        # Connect to ODrive boards
        radius_board = odrive.find_any(serial_number="208F3388304B")
        theta_board = odrive.find_any(serial_number="388937553437")

        # Make sure that everything is okay with the brake resistors
        assert theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."
        assert radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

        # Connect to the actual ODrive motors through ODrive_Axis objects
        theta_motor = ODrive_Ease_Lib.ODrive_Axis(theta_board.axis0, 10, 30)
        r1 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis0, 20, 20)  # Blue tape #
        r2 = ODrive_Ease_Lib.ODrive_Axis(radius_board.axis1, 20, 20)  # Orange tape

        # Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
        # are calibrated.
        while not (r1.is_calibrated() and r2.is_calibrated()):
            radius_board.reboot()
        while not theta_motor.is_calibrated():
            theta_board.reboot()
        print("All motors are calibrated!")
