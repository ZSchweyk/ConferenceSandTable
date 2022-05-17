import odrive
import ODrive_Ease_Lib
import time



class RadiiMotors:
    homing_speed = 5
    rotations_from_center = 2

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
        self.r1.set_vel(self.homing_speed)
        self.r2.set_vel(self.homing_speed)

        while self.r1.is_busy() or self.r2.is_busy():  # must wait for both radius motors to stop moving
            pass
        time.sleep(1)
        self.r1.set_relative_pos(-self.rotations_from_center)
        # TODO self.r1.set_home_to(self.r1.get_raw_pos() - self.rotations_from_center)
        self.r1.set_home()

        time.sleep(1)
        self.r2.set_relative_pos(-self.rotations_from_center)
        # TODO self.r2.set_home_to(self.r1.get_raw_pos() - self.rotations_from_center)
        self.r2.set_home()

        time.sleep(1)


