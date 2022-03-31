import time
import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from math import *


table = ConferenceSandTable()
# table.home()
# table.find_ball()

# table.emergency_stop()

table.draw_equation("sin(10 * theta)", 2 * pi, theta_speed=.5, scale_factor=1, sleep=.005)

print("\n" * 10)
table.r1.idle()
table.r2.idle()
table.theta_motor.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)
ODrive_Ease_Lib.dump_errors(table.theta_board)
