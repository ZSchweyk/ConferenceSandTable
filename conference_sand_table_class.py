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
        self.radius_board = odrive.find_any(serial_number="208F3388304B")
        self.theta_board = odrive.find_any(serial_number="388937553437")

        # Make sure that everything is okay with the brake resistors
        assert self.theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."
        assert self.radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

        # Connect to the actual ODrive motors through ODrive_Axis objects
        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_board.axis0, 10, 30)
        self.r1 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis0, 20, 20)  # Blue tape #
        self.r2 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis1, 20, 20)  # Orange tape

        # Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
        # are calibrated.
        while not (self.r1.is_calibrated() and self.r2.is_calibrated()):
            self.radius_board.reboot()
        while not self.theta_motor.is_calibrated():
            self.theta_board.reboot()
        print("All motors are calibrated!")

    def set_mode(self, mirror=False):
        if mirror:
            self.r2.axis.controller.config.axis_to_mirror = 0
            self.r2.axis.controller.config.input_mode = 7
            self.r2.axis.requested_state = 8





