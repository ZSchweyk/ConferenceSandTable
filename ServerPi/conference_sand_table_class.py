import time
from settings import *
from math import *
import numpy as np
import odrive
import ODrive_Ease_Lib as ODrive_Ease_Lib
from server import ThetaServer


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


class ConferenceSandTable:
    gear_ratio = 562.5  # (90/15)×(90/15)×(90÷18)×(50/16)
    radius_motor_max_rotations = 25
    rotations_from_center = 2  # TODO: test out making this smaller (1.5 maybe)
    homing_speed = 5

    def __init__(self, server_ip):
        print("Attempting to connect to theta board")
        self.theta_board = odrive.find_any(serial_number="388937553437")
        print("Connected to theta board")

        # Make sure that everything is okay with the brake resistors
        assert self.theta_board.config.enable_brake_resistor, "Check for faulty theta brake resistor."

        self.theta_board.clear_errors()

        self.theta_motor = ODrive_Ease_Lib.ODrive_Axis(self.theta_board.axis0, current_lim=30, vel_lim=30)

        while not self.theta_motor.is_calibrated():
            # self.theta_motor.calibrate_encoder()
            self.theta_motor.calibrate()
            # self.theta_board.reboot()
            print("Calibrated theta")
        print("Finished Calibrating Theta Board")

        self.theta_motor.axis.controller.config.enable_overspeed_error = False

        self.radius_motors_homed = False

        self.server = ThetaServer(server_ip)
        print("Theta Server going")

    def home_radius_motors(self):
        self.server.send_to_radius_client({"method": "home"})

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
            self.home_radius_motors()

        assert 0 <= theta_speed <= 1, "Incorrect theta_speed bounds. Must be between 0 and 1."

    @staticmethod
    def get_theta_range(equation, count_accuracy=10):
        theta = 0
        theta_increment = pi / 100
        cartesian_coordinates = []
        count = 0
        while True:
            r = eval(equation)
            x, y = r * cos(theta), r * sin(theta)
            if (x, y) in cartesian_coordinates:
                count += 1
            else:
                count = 0

            if count == count_accuracy:
                return theta

            cartesian_coordinates.append((x, y))
            theta += theta_increment


    def draw_equation(self, equation: str, period, theta_speed=.75, scale_factor=1, sleep=.005):
        method_start_time = time.perf_counter()
        self.pre_check(equation, theta_speed)

        theta_speed = theta_speed * (
                self.theta_motor.get_vel_limit() * CAP_THETA_VELOCITY_AT)  # capped max vel to 85% of max speed
        # because I don't want to lose connection to the motor

        scale_factor = max(min(scale_factor, 1), 0)  # This bounds scale_factor between 0 and 1

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



        time_intervals = [sleep + .04]
        self.theta_motor.set_home()
        print("theta motor homed")
        self.theta_motor.set_vel(theta_speed)
        print("set vel to theta motor")
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
            dict_of_points = {}
            if r1 >= 0:
                r1 = max(r1, self.rotations_from_center)
                r2 = max(r2, self.rotations_from_center)
                dict_of_points["points"] = [("r1", -r1, bandwidth), ("r2", -r2, bandwidth)]
                # self.r1.set_pos_filter(-r1, bandwidth)
                # self.r2.set_pos_filter(-r2, bandwidth)
            else:
                r1 = min(r1, -self.rotations_from_center)
                r2 = min(r2, -self.rotations_from_center)
                dict_of_points["points"] = [("r1", r2, bandwidth), ("r2", r1, bandwidth)]
                # self.r1.set_pos_filter(r2, bandwidth)
                # self.r2.set_pos_filter(r1, bandwidth)

            self.server.send_to_radius_client(dict_of_points)
            # self.r2.wait() Does not work with set_pos_filter
            time.sleep(sleep)
            end = time.perf_counter()
            time_intervals.append(end - start)
            # print("Duration:", end - start)

        self.theta_motor.set_vel(0)
        # print(np.diff(previous_thetas))
        method_end_time = time.perf_counter()
        self.server.send_to_radius_client("Disconnect")

        return {
            "Time Taken": method_end_time - method_start_time,  # seconds
            "Average Time Difference": np.mean(time_intervals),
            "Average Angle Difference": np.mean(np.diff(previous_thetas)),
            "Min Angle Difference": min(np.diff(previous_thetas)),
            "Max Angle Difference": max(np.diff(previous_thetas)),
        }






# s = ThetaServer()
# for i in range(1, 101):
#     s.send_to_radius_client(i)
#
# s.send_to_radius_client("Close Connection")
#
# s.close_server()










# def run_server(equation: str, period, theta_speed=.75, scale_factor=1, sleep=.005):
#     assert validation.is_equation_valid(equation), "Invalid Equation"
#     assert 0 <= theta_speed <= 1, "Incorrect theta_speed bounds. Must be between 0 and 1."
#     scale_factor = max(min(scale_factor, 1), 0)
#
#
#
#     # Find min and max radii for r1 and r2 to scale properly below.
#     all_r1_values = []
#     all_r2_values = []
#     for theta1 in np.arange(0, period / 2, pi / 100):
#         theta2 = theta1 + pi
#         r1 = eval(equation.replace("theta", "theta1"))
#         r2 = eval(equation.replace("theta", "theta2"))
#         if (round(r1, 3) >= 0) != (round(r2, 3) >= 0):
#             print("Drawing with only 1 motor!")
#             return self.draw_equation_with_1_motor(equation, period, theta_speed=theta_speed,
#                                                    scale_factor=scale_factor,
#                                                    sleep=sleep)
#
#         all_r1_values.append(r1)
#         all_r2_values.append(r2)
#
#     smallest_r1, largest_r1 = min(all_r1_values), max(all_r1_values)
#     smallest_r2, largest_r2 = min(all_r2_values), max(all_r2_values)
#
#
#     theta_speed = theta_speed * (
#             self.theta_motor.get_vel_limit() * CAP_THETA_VELOCITY_AT)  # capped max vel to 85% of max speed
#     # because I don't want to lose connection to the motor
