import time
import ODrive_Ease_Lib

from conference_sand_table_class import ConferenceSandTable
from math import pi
from server import ThetaServer


try:
    table = ConferenceSandTable("localhost")
    table.draw_equation("10 * sin(6 * theta)", 2*pi, theta_speed=.4, scale_factor=1, sleep=.005)
finally:
    table.theta_motor.idle()
    ODrive_Ease_Lib.dump_errors(table.theta_board)
    table.theta_motor.clear_errors()
    table.server.close_server()


