import time

from conference_sand_table_class import ConferenceSandTable
from math import pi
from server import ThetaServer


try:
    table = ConferenceSandTable()
    table.draw_equation("10 * sin(6 * theta)", 2*pi, .75, 1, sleep=.005)
finally:
    table.server.close_server()

# server = ThetaServer("localhost")
#
# for i in range(2, 1000):
#     print("sending", i)
#     server.send_to_radius_client(str(i))
#     time.sleep(1)
#
# time.sleep(10)
