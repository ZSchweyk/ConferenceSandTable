import time

from conference_sand_table_class import ConferenceSandTable
from math import pi
from server import ThetaServer


try:
    table = ConferenceSandTable("localhost")
    table.draw_equation("10 * sin(6 * theta)", .25*pi, .75, 1, sleep=.005)
finally:
    table.server.close_server()


