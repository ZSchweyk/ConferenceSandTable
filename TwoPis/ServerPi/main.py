import time
import ODrive_Ease_Lib

from conference_sand_table_class import ConferenceSandTable
from math import pi
from server import ThetaServer



def draw_equation(equation, theta_range, theta_speed, scale_factor):
    try:
        table = ConferenceSandTable("localhost")
        table.draw_equation(equation, theta_range, theta_speed=theta_speed, scale_factor=scale_factor, sleep=.005)
    finally:
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.theta_board)
        table.theta_motor.clear_errors()
        table.server.close_server()


