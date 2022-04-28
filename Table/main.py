import time
import Table.ODrive_Ease_Lib as ODrive_Ease_Lib
from Table.conference_sand_table_class import ConferenceSandTable
from math import *


if __name__ == "__main__":
    table = ConferenceSandTable()
    try:

        table.home()
        # table.find_ball()

        # table.emergency_stop()

        info = table.draw_equation("2 * sin(5.4 * theta)", 1 * pi, theta_speed=.7, scale_factor=1, sleep=.005)

        print("info:", info)

        # info = table.draw_equation("sin(6 * theta)", 2 * pi, theta_speed=.9, scale_factor=1, sleep=.005)
        #
        # print("info:", info)
        #
        # info = table.draw_equation("2 * sin(5.4 * theta)", 5 * pi, theta_speed=.6, scale_factor=1, sleep=.005)
        #
        # print("info:", info)
        #
        # info = table.draw_equation("theta * sin(3 * theta)", 12 * pi, theta_speed=.75, scale_factor=1, sleep=.005)
        #
        # print("info:", info)

        print("\n" * 10)
        table.r1.idle()
        table.r2.idle()
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.radius_board)
        ODrive_Ease_Lib.dump_errors(table.theta_board)

        table.radius_board.clear_errors()
        table.theta_motor.clear_errors()
    except KeyboardInterrupt as e:
        print(e)
        table.emergency_stop()
