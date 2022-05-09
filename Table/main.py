import sys
sys.path.append("~/projects/ConferenceSandTable/Table")
import time
import ODrive_Ease_Lib as ODrive_Ease_Lib
from conference_sand_table_class import ConferenceSandTable
from email_script import send_email
import os
from math import *


if __name__ == "__main__":
    table = ConferenceSandTable()
    try:
        table.home()
        angle = pi/2
        for i in range(25):
            print(i+1)
            table.rotate(angle)
            angle *= -1
            table.move("out")
            table.move("in")

    except KeyboardInterrupt as e:
        table.emergency_stop()
        for email in ["zeynschweyk@dpengineering.org", "zschweyk@gmail.com"]:
            send_email(
                os.environ["EMAIL_ADDRESS"],
                os.environ["EMAIL_ADDRESS_PASSWORD"],
                email,
                "ConferenceSandTable Error",
                "The ConferenceSandTable's radius board lost connection!",
                ""
            )
    finally:
        table.r1.idle()
        table.r2.idle()
        table.theta_motor.idle()
        ODrive_Ease_Lib.dump_errors(table.radius_board)
        ODrive_Ease_Lib.dump_errors(table.theta_board)

        table.radius_board.clear_errors()
        table.theta_motor.clear_errors()
