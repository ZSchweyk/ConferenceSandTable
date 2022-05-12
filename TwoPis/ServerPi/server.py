import enum
import pickle
import sys
from math import *
# import numpy as np
sys.path.append("~/projects/ConferenceSandTable/TwoPis")
from server_class import Server
import validation
from settings import *


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


class ThetaServer:
    def __init__(self):
        #         |Bind IP       |Port |Packet enum
        self.s = Server("172.17.21.1", 5001, PacketType)
        self.s.open_server()
        self.s.wait_for_connection()

    def send_to_radius_client(self, info):
        self.s.send_packet(PacketType.COMMAND2, pickle.dumps(info))
        assert pickle.loads(self.s.recv_packet()[1]) == info, "Could not send packet"

    def close_server(self):
        self.s.close_connection()
        self.s.close_server()
        print("Server has been stopped")



s = ThetaServer()
for i in range(1, 101):
    s.send_to_radius_client(i)

s.send_to_radius_client("Close Connection")

s.close_server()




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









