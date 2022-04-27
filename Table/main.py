import time
import Table.ODrive_Ease_Lib as ODrive_Ease_Lib
from Table.conference_sand_table_class import ConferenceSandTable
from math import *


table = ConferenceSandTable()
table.home()
# table.find_ball()

# table.emergency_stop()

info = table.draw_equation("sin(6 * theta)", 2 * pi, theta_speed=.25, scale_factor=1, sleep=.005)

print("info:", info)

print("\n" * 10)
table.r1.idle()
table.r2.idle()
table.theta_motor.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)
ODrive_Ease_Lib.dump_errors(table.theta_board)

table.radius_board.clear_errors()
table.theta_motor.clear_errors()
