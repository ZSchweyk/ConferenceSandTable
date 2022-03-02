import time
import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable

table = ConferenceSandTable()

table.move("out")

table.find_ball()

# table.theta_motor.set_vel(15)  # might have to change this value
# time.sleep(5)
# table.theta_motor.set_vel(0)

table.r1.idle()
table.r2.idle()
table.theta_motor.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)
ODrive_Ease_Lib.dump_errors(table.theta_board)
