import sys
sys.path.append("~/projects/ConferenceSandTable/Table")
import time
import ODrive_Ease_Lib as ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from math import *


if __name__ == "__main__":
    table = ConferenceSandTable()
    try:
        table.home()
        while True:
            table.move("out")
            time.sleep(4)
            table.move("in")
            time.sleep(4)



    except KeyboardInterrupt as e:
        table.emergency_stop()
    finally:
        table.r1.idle()
        table.r2.idle()
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.radius_board)
        ODrive_Ease_Lib.dump_errors(table.theta_board)

        table.radius_board.clear_errors()
        table.theta_motor.clear_errors()
