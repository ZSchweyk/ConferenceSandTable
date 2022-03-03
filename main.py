import time
import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from math import *
table = ConferenceSandTable()

# table.move("out")
table.home()

table.draw_equation("sin(theta)", pi)

print("\n" * 10)
table.r1.idle()
table.r2.idle()
table.theta_motor.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)
ODrive_Ease_Lib.dump_errors(table.theta_board)
