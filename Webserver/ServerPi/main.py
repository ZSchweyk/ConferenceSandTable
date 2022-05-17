import time

import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from math import pi


def draw_equation(table: ConferenceSandTable, equation, theta_range, theta_speed, scale_factor):
    try:
        table.draw_equation(equation, theta_range, theta_speed=theta_speed, scale_factor=scale_factor)
        print("Finished sending over equation values")
    finally:
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.theta_board)
        table.theta_motor.clear_errors()
        time.sleep(6)
        table.server.close_server()
        print("Server closed")


draw_equation(equation="10 * sin(6.2 * theta)", theta_range=5 * pi, theta_speed=.6, scale_factor=1)



