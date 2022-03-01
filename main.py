import time

import ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable

table = ConferenceSandTable()

table.move("out")
table.move("in")
table.move("out")

print("About to home...")

# direction = "out"
# while True:
#     table.move(direction)
#     direction = "in" if direction == "out" else "out"
#     time.sleep(1.5)

table.home()
table.r1.idle()
table.r2.idle()

ODrive_Ease_Lib.dump_errors(table.radius_board)

