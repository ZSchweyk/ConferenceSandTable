import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os
from math import *


class ConferenceSandTable:
    def __init__(self):
        # Occasionally, it can't connect to radius_board. Power cycling seems like a temporary fix, but I'm not sure
        # what to do.

        # Connect to ODrive boards
        print("Connecting to boards...")
        self.radius_board = odrive.find_any(serial_number="208F3388304B")
        print("Connected to radius board")
        self.theta_board = odrive.find_any(serial_number="388937553437")
        print("Connected to theta board")
        print("Found both boards")

        # Make sure that everything is okay with the brake resistors
        assert self.theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."
        assert self.radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

        self.radius_board.clear_errors()


        # Connect to the actual ODrive motors through ODrive_Axis objects
        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_board.axis0, 10, 30)
        self.r1 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis0, 20, 20)  # Blue tape #
        self.r2 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis1, 20, 20)  # Orange tape

        # Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
        # are calibrated.
        while not (self.r1.is_calibrated() and self.r2.is_calibrated()):
            self.r1.calibrate_encoder()
            self.r2.calibrate_encoder()
            # self.radius_board.reboot()
            time.sleep(10)
        while not self.theta_motor.is_calibrated():
            self.theta_motor.calibrate_encoder()
            # self.theta_board.reboot()
            time.sleep(10)
        print("All motors are calibrated!")

    def set_mode(self, mirror=False):
        """Probably don't need to use mirror mode, but I added it just in case"""
        if mirror:
            self.r2.axis.controller.config.axis_to_mirror = 0
            self.r2.axis.controller.config.input_mode = 7
            self.r2.axis.requested_state = 8

    def move(self, in_or_out):
        if in_or_out == "in":
            self.r1.set_rel_pos_traj(25, 10, 15, 10)
            self.r2.set_rel_pos_traj(25, 10, 15, 10)
        elif in_or_out == "out":
            self.r1.set_rel_pos_traj(-25, 10, 15, 10)
            self.r2.set_rel_pos_traj(-25, 10, 15, 10)
        self.r2.wait()

    def home(self):
        self.r1.set_vel(10)
        self.r2.set_vel(10)

        while self.r2.is_busy():
            pass
        self.r1.set_vel(0)
        self.r1.set_home()

        self.r2.set_vel(0)
        self.r2.set_home()

    def find_ball(self):
        # This is starter code for homing. I will probably have to adjust constants
        self.home()

        self.theta_motor.set_vel(15)  # might have to change this value
        self.r1.set_vel(-1.6)
        self.r2.set_vel(-1.6)
        time.sleep(1)

        while self.r2.is_busy() or self.r1.is_busy():
            pass
        print("Motors reached the end")
        self.r1.set_vel(0)
        self.r2.set_vel(0)
        self.theta_motor.set_vel(0)



    def draw_equation(self, equation: str, period):
        builtin_restrictions = {
            "min": min,
            "max": max,
        }
        other_restrictions = {
            "sqrt": sqrt,
            "sin": sin,
            "cos": cos,
        }
        start_time = time.perf_counter()
        print("start_time", start_time)
        start_pos = self.theta_motor.get_pos()
        print("start_pos", start_pos)
        self.theta_motor.set_vel(10)
        while self.theta_motor.is_busy():
            print(self.theta_motor.get_pos())
            if self.theta_motor.get_pos() - start_pos >= start_pos:
                print(time.perf_counter() - start_time)
                self.theta_motor.set_vel(0)
                break

    def stop_theta(self):
        self.theta_motor.set_vel(0)





