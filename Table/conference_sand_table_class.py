import sys
sys.path.append("~/projects/ConferenceSandTable/Table")
import odrive
import usb.core
import ODrive_Ease_Lib
import numpy as np
import time
import os
from math import *
from settings import *
from odrive.utils import start_liveplotter


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


class ConferenceSandTable:
    # 562.5 rotations of the small gear right above the theta motor corresponds to 1 full revolution of the table's arm
    gear_ratio = 562.5  # (90/15)×(90/15)×(90÷18)×(50/16)
    radius_motor_max_rotations = 25
    rotations_from_center = 2  # TODO: test out making this smaller (1.5 maybe)
    homing_speed = 5

    def __init__(self):
        # Occasionally, it can't connect to radius_board. Power cycling seems like a temporary fix, but I'm not sure
        # what to do. Another temporary fix is to unplug the fuse for the radius board and plug it back in.

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
        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_board.axis0, current_lim=30, vel_lim=30)
        self.r1 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis0, current_lim=30, vel_lim=30)  # Blue tape
        self.r2 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis1, current_lim=30, vel_lim=30)  # Orange tape

        # self.r1.axis.controller.config.enable_overspeed_error = False
        # self.r2.axis.controller.config.enable_overspeed_error = False

        # Ensure that all motors are calibrated (which should be completed upon startup). Reboot ODrives until they
        # are calibrated.
        while not (self.r1.is_calibrated() and self.r2.is_calibrated()):
            self.r1.calibrate_encoder()
            self.r2.calibrate_encoder()
            # self.radius_board.reboot()
            print("Calibrated r1 and r2")
            # time.sleep(10)
        while not self.theta_motor.is_calibrated():
            self.theta_motor.calibrate_encoder()
            # self.theta_board.reboot()
            print("Calibrated theta")
            # time.sleep(10)
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
            self.r1.set_rel_pos_traj(self.radius_motor_max_rotations-1, 10, 15, 10)
            self.r2.set_rel_pos_traj(self.radius_motor_max_rotations-1, 10, 15, 10)
        elif in_or_out == "out":
            self.r1.set_rel_pos_traj(-self.radius_motor_max_rotations+1, 10, 15, 10)
            self.r2.set_rel_pos_traj(-self.radius_motor_max_rotations+1, 10, 15, 10)

        while self.r1.is_busy() or self.r2.is_busy():
            pass

    def home(self):
        self.r1.set_vel(self.homing_speed)
        self.r2.set_vel(self.homing_speed)

        while self.r1.is_busy() or self.r2.is_busy():  # must wait for both radius motors to stop moving
            pass
        time.sleep(1)
        self.r1.set_relative_pos(-self.rotations_from_center)
        # TODO self.r1.set_home_to(self.r1.get_raw_pos() - self.rotations_from_center)
        self.r1.set_home()

        time.sleep(1)
        self.r2.set_relative_pos(-self.rotations_from_center)
        # TODO self.r2.set_home_to(self.r1.get_raw_pos() - self.rotations_from_center)
        self.r2.set_home()

        time.sleep(1)
        self.radius_motors_homed = True

    def find_ball(self):
        # This is starter code for homing. I will probably have to adjust constants
        if not self.radius_motors_homed:
            self.home()

        self.theta_motor.set_vel(15)  # TODO might have to change this value
        self.r1.set_vel(-1.6)
        self.r2.set_vel(-1.6)
        time.sleep(1)

        while self.r2.is_busy() or self.r1.is_busy():
            pass
        self.r1.set_vel(0)
        self.r2.set_vel(0)
        self.theta_motor.set_vel(0)

    def rotate(self, rads, wait=True):
        self.theta_motor.set_rel_pos_traj(rads / (2 * pi) * self.gear_ratio, 10, 15, 10)
        if wait:
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

    def pre_check(self, equation, theta_speed):
        if not self.is_equation_valid(equation):
            raise Exception("Invalid Equation")

        if not self.radius_motors_homed:
            self.home()

        assert 0 <= theta_speed <= 1, "Incorrect theta_speed bounds. Must be between 0 and 1."

    def draw_equation_with_1_motor(self, equation: str, period, theta_speed=.75, scale_factor=1, sleep=.005):
        method_start_time = time.perf_counter()  # start timing how long the method takes
        self.pre_check(equation, theta_speed)  # validate inputs

        theta_speed = theta_speed * (
                self.theta_motor.get_vel_limit() * CAP_THETA_VELOCITY_AT)  # capped max vel to 85% of max speed
        # because I don't want to lose connection to the motor

        scale_factor = max(min(scale_factor, 1), 0)  # This bounds scale_factor between 0 and 1

        all_r_values = [eval(equation) for theta in np.arange(0, period, pi / 100)]  # calculate all r values

        # find the range of the r values to later deal with scaling them properly.
        smallest_r, largest_r = min(all_r_values), max(all_r_values)

        time_intervals = [sleep + .04]
        self.theta_motor.set_home()
        self.theta_motor.set_vel(theta_speed)
        max_rotations = self.gear_ratio * period / (2 * pi)
        previous_thetas = [0]
        self.r2.set_pos(0)
        while self.theta_motor.get_pos() < max_rotations:
            start = time.perf_counter()

            percent_complete = self.theta_motor.get_pos() / max_rotations
            print("Percent Complete: " + str(round(percent_complete * 100, 2)) + "%")

            theta = self.theta_motor.get_pos() / self.gear_ratio * 2 * pi
            previous_thetas.append(theta * 180 / pi)
            # print("theta1", theta1 * 180 / pi)

            r = eval(equation)
            r = scale(r, smallest_r, largest_r, -self.radius_motor_max_rotations * scale_factor,
                      self.radius_motor_max_rotations * scale_factor)

            bandwidth = (1 / np.mean(time_intervals))
            # print("bandwidth", bandwidth)
            if r >= 0:
                # print("+")
                r = max(r, self.rotations_from_center)
                self.r1.set_pos_filter(-r, bandwidth)
            else:
                # print("-")
                r = min(r, -self.rotations_from_center)
                self.r2.set_pos_filter(r, bandwidth)
            # self.r2.wait() Does not work with set_pos_filter
            time.sleep(sleep)
            end = time.perf_counter()
            time_intervals.append(end - start)
            # print("Duration:", end - start)

        self.theta_motor.set_vel(0)
        # print(np.diff(previous_thetas))
        method_end_time = time.perf_counter()
        return {
            "Time Taken": method_end_time - method_start_time,  # seconds
            "Average Time Difference": np.mean(time_intervals),
            "Average Angle Difference": np.mean(np.diff(previous_thetas)),
            "Min Angle Difference": min(np.diff(previous_thetas)),
            "Max Angle Difference": max(np.diff(previous_thetas)),
            "STD Angle Difference": np.std(np.diff(previous_thetas))
        }

    def draw_equation(self, equation: str, period, theta_speed=.75, scale_factor=1, sleep=.005):
        method_start_time = time.perf_counter()
        self.pre_check(equation, theta_speed)

        # Find min and max radii for r1 and r2 to scale properly below.
        all_r1_values = []
        all_r2_values = []
        for theta1 in np.arange(0, period / 2, pi / 100):
            theta2 = theta1 + pi
            r1 = eval(equation.replace("theta", "theta1"))
            r2 = eval(equation.replace("theta", "theta2"))
            if (round(r1, 3) >= 0) != (round(r2, 3) >= 0):
                print("Drawing with only 1 motor!")
                return self.draw_equation_with_1_motor(equation, period, theta_speed=theta_speed,
                                                       scale_factor=scale_factor,
                                                       sleep=sleep)

            all_r1_values.append(r1)
            all_r2_values.append(r2)

        smallest_r1, largest_r1 = min(all_r1_values), max(all_r1_values)
        smallest_r2, largest_r2 = min(all_r2_values), max(all_r2_values)

        # print("smallest_r1", smallest_r1)
        # print("largest_r1", largest_r1)
        #
        # print("smallest_r2", smallest_r2)
        # print("largest_r2", largest_r2)

        theta_speed = theta_speed * (
                self.theta_motor.get_vel_limit() * CAP_THETA_VELOCITY_AT)  # capped max vel to 85% of max speed
        # because I don't want to lose connection to the motor

        scale_factor = max(min(scale_factor, 1), 0)  # This bounds scale_factor between 0 and 1

        time_intervals = [sleep + .04]
        self.theta_motor.set_home()
        self.theta_motor.set_vel(theta_speed)
        max_rotations = self.gear_ratio * .5 * period / (2 * pi)
        previous_thetas = [0]
        while self.theta_motor.get_pos() < max_rotations:
            start = time.perf_counter()
            percent_complete = self.theta_motor.get_pos() / max_rotations
            print("Percent Complete: " + str(round(percent_complete * 100, 2)) + "%")
            theta1 = self.theta_motor.get_pos() / self.gear_ratio * 2 * pi
            theta2 = theta1 + pi
            previous_thetas.append(theta1 * 180 / pi)
            # print("theta1", theta1 * 180 / pi)

            r1 = eval(equation.replace("theta", "theta1"))
            r2 = eval(equation.replace("theta", "theta2"))

            r1 = scale(r1, smallest_r1, largest_r1, -self.radius_motor_max_rotations * scale_factor,
                       self.radius_motor_max_rotations * scale_factor)
            r2 = scale(r2, smallest_r2, largest_r2, -self.radius_motor_max_rotations * scale_factor,
                       self.radius_motor_max_rotations * scale_factor)

            bandwidth = (1 / np.mean(time_intervals))
            if r1 >= 0:
                r1 = max(r1, self.rotations_from_center)
                r2 = max(r2, self.rotations_from_center)
                self.r1.set_pos_filter(-r1, bandwidth)
                self.r2.set_pos_filter(-r2, bandwidth)
            else:
                r1 = min(r1, -self.rotations_from_center)
                r2 = min(r2, -self.rotations_from_center)
                self.r1.set_pos_filter(r2, bandwidth)
                self.r2.set_pos_filter(r1, bandwidth)
            # self.r2.wait() Does not work with set_pos_filter
            time.sleep(sleep)
            end = time.perf_counter()
            time_intervals.append(end - start)
            # print("Duration:", end - start)

        self.theta_motor.set_vel(0)
        # print(np.diff(previous_thetas))
        method_end_time = time.perf_counter()
        return {
            "Time Taken": method_end_time - method_start_time,  # seconds
            "Average Time Difference": np.mean(time_intervals),
            "Average Angle Difference": np.mean(np.diff(previous_thetas)),
            "Min Angle Difference": min(np.diff(previous_thetas)),
            "Max Angle Difference": max(np.diff(previous_thetas)),
        }

    def emergency_stop(self):
        print("Stopping motors..")
        self.theta_motor.set_vel(0)
        self.r1.set_relative_pos(0)
        self.r1.set_relative_pos(0)
        print("Stopped")
