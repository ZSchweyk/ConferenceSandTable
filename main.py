import time
import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable

table = ConferenceSandTable()

table.move("out")

print("About to home...")

table.home()

table.r1.idle()
table.r2.idle()
ODrive_Ease_Lib.dump_errors(table.radius_board)

