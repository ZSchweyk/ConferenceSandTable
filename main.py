import time

from conference_sand_table_class import ConferenceSandTable

table = ConferenceSandTable()
# table.draw_equation("", 1)
# time.sleep(5)
# table.stop_theta()

direction = "out"
while True:
    table.move(direction)
    direction = "in" if direction == "out" else "out"
    time.sleep(1.5)


