import time

import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from server import ThetaServer
from math import pi


def draw_equation(equation, theta_range, theta_speed, scale_factor):
    try:
        table = ConferenceSandTable("172.17.21.2")
        table.draw_equation(equation, theta_range, theta_speed=theta_speed, scale_factor=scale_factor, sleep=.005)
    finally:
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.theta_board)
        table.theta_motor.clear_errors()
        table.server.close_server()


# draw_equation("10 * sin(6 * theta)", 2 * pi, .6, 1)

try:
    server = ThetaServer("172.17.21.2")
    start = time.perf_counter()
    server.send_to_radius_client("test packet")
    server.receive_from_radius_client()
    end = time.perf_counter()
    server.send_to_radius_client("Disconnect")
    print("One packet took", (end-start)/2, "seconds to send.")

finally:
    server.close_server()



