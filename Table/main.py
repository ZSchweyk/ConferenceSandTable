import time
import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from math import *


table = ConferenceSandTable()
# table.home()
# table.find_ball()

table.draw_equation("4*sin(4.3 * theta)", 12 * pi, theta_speed=1, scale_factor=1)

print("\n" * 10)
table.r1.idle()
table.r2.idle()
table.theta_motor.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)
ODrive_Ease_Lib.dump_errors(table.theta_board)
