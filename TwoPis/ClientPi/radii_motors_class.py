import sys
sys.path.append("~/projects/ConferenceSandTable/TwoPis")
from client import RadiusClient
import odrive
import usb.core
import TwoPis.ODrive_Ease_Lib as ODrive_Ease_Lib



class RadiiMotors:
    def __init__(self):
        self.radius_board = odrive.find_any(serial_number="208F3388304B")
        print("Connected to radius board")

        assert self.radius_board.config.enable_brake_resistor, "Check for faulty radius brake resistor."

        self.r1 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis0, current_lim=30, vel_lim=30)  # Blue tape
        self.r2 = ODrive_Ease_Lib.ODrive_Axis(self.radius_board.axis1, current_lim=30, vel_lim=30)  # Orange tape

        while not (self.r1.is_calibrated() and self.r2.is_calibrated()):
            self.r1.calibrate_encoder()
            self.r2.calibrate_encoder()
            print("Calibrated r1 and r2")
        print("Finished Calibrating r1 and r2")

    def home(self):
        pass


method_list = [attribute for attribute in dir(RadiiMotors) if callable(getattr(RadiiMotors, attribute)) and not attribute.startswith('__')]
print(method_list)


# c = RadiusClient()
# is_running = True
# while is_running:
#     is_running = c.start_listening()
#
# print("Client finished running")