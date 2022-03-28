import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os
from math import *


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


class ConferenceSandTable:
    # 562.5 rotations of the small gear right above the theta motor corresponds to 1 full revolution of the table's arm
    gear_ratio = 562.5  # (90/15)×(90/15)×(90÷18)×(50/16)

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
        self.theta_board.clear_errors()

        # Connect to the actual ODrive motors through ODrive_Axis objects
        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_board.axis0, 20, 30)
        self.r1 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis0, 20, 30)  # Blue tape
        self.r2 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis1, 20, 30)  # Orange tape

        # Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
        # are calibrated.
        while not (self.r1.is_calibrated() and self.r2.is_calibrated()):
            self.r1.calibrate_encoder()
            self.r2.calibrate_encoder()
            # self.radius_board.reboot()
            print("Calibrated r1 and r2")
            time.sleep(10)
        while not self.theta_motor.is_calibrated():
            self.theta_motor.calibrate_encoder()
            # self.theta_board.reboot()
            print("Calibrated theta")
            time.sleep(10)
        print("All motors are calibrated!")

        self.radius_motors_homed = False

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

        self.radius_motors_homed = True

    def find_ball(self):
        # This is starter code for homing. I will probably have to adjust constants
        if not self.radius_motors_homed:
            self.home()

        self.theta_motor.set_vel(15)  # might have to change this value
        self.r1.set_vel(-1.6)
        self.r2.set_vel(-1.6)
        time.sleep(1)

        while self.r2.is_busy() or self.r1.is_busy():
            pass
        self.r1.set_vel(0)
        self.r2.set_vel(0)
        self.theta_motor.set_vel(0)

    def rotate(self, rads):
        self.theta_motor.set_relative_pos(rads / (2 * pi) * self.gear_ratio)
        self.theta_motor.wait()

    @staticmethod
    def is_equation_valid(equation):
        builtin_restrictions = {
            "min": min,
            "max": max,
        }
        other_restrictions = {
            "sqrt": sqrt,
            "sin": sin,
            "cos": cos,
        }
        theta = 0
        other_restrictions["theta"] = theta

        try:
            eval(equation, {"__builtins__": builtin_restrictions}, other_restrictions)
        except Exception as exception:
            return False
        return True

    def calculate_period(self, equation):
        if not self.is_equation_valid(equation):
            raise Exception("Invalid Equation")

        theta = 0
        coordinates = []
        while True:

            r = eval(equation)
            print((theta, r))
            if (theta - (2 * pi), r) in coordinates:
                return theta
            coordinates.append((theta, r))
            theta += .001


    def draw_equation(self, equation: str, period, theta_speed=5, scale_factor=1):
        if not self.is_equation_valid(equation):
            raise Exception("Invalid Equation")

        if not self.radius_motors_homed:
            self.home()

        # Find min and max radii for r1 and r2 to scale properly below.
        all_r1_values = []
        all_r2_values = []
        for theta1 in np.arange(0, period / 2, pi / 100):
            theta2 = theta1 + pi
            r1 = eval(equation.replace("theta", "theta1"))
            r2 = eval(equation.replace("theta", "theta2"))
            # print(theta1, theta2)
            # print(round(r1, 3), round(r2, 3))
            assert ((round(r1, 3) >= 0) == (
                    round(r2, 3) >= 0)), "Cannot draw the equation \"" + equation + "\", since motors would have " \
                                                                                    "to be at 2 places at once."
            all_r1_values.append(r1)
            all_r2_values.append(r2)

        smallest_r1, largest_r1 = min(all_r1_values), max(all_r1_values)
        smallest_r2, largest_r2 = min(all_r2_values), max(all_r2_values)

        # print("smallest_r1", smallest_r1)
        # print("largest_r1", largest_r1)
        #
        # print("smallest_r2", smallest_r2)
        # print("largest_r2", largest_r2)

        scale_factor = max(min(scale_factor, 1), 0)  # This bounds scale_factor between 0 and 1

        self.theta_motor.set_home()
        self.theta_motor.set_vel(theta_speed)
        max_rotations = self.gear_ratio * .5 * period / (2 * pi)
        previous_thetas = [0]
        while self.theta_motor.get_pos() < max_rotations:
            start = time.perf_counter()
            theta1 = self.theta_motor.get_pos() / self.gear_ratio * 2 * pi
            theta2 = theta1 + pi
            previous_thetas.append(theta1 * 180 / pi)
            print("theta1", theta1 * 180 / pi)

            r1 = eval(equation.replace("theta", "theta1"))
            r2 = eval(equation.replace("theta", "theta2"))

            r1 = scale(r1, smallest_r1, largest_r1, -25 * scale_factor, 25 * scale_factor)
            r2 = scale(r2, smallest_r2, largest_r2, -25 * scale_factor, 25 * scale_factor)
            if r1 >= 0:
                self.r1.set_pos_traj(-r1, 25, 25, 25)
                self.r2.set_pos_traj(-r2, 25, 25, 25)
            else:
                self.r1.set_pos_traj(r2, 25, 25, 25)
                self.r2.set_pos_traj(r1, 25, 25, 25)
            self.r2.wait()
            end = time.perf_counter()
            print("Duration:", end - start)

        self.theta_motor.set_vel(0)
        print(np.diff(previous_thetas))
        print("Average Difference:", np.mean(np.diff(previous_thetas)))
        print("Min Difference:", min(np.diff(previous_thetas)))
        print("Max Difference:", max(np.diff(previous_thetas)))
        print("STD Difference:", np.std(np.diff(previous_thetas)))
