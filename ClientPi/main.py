from datetime import datetime

with open("/home/pi/projects/log.txt", "a") as file:
    file.write("Created file at " + datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))

import time
import ODrive_Ease_Lib
from radii_motors_class import RadiiMotors
from client import RadiusClient

# method_list = [attribute for attribute in dir(RadiiMotors) if callable(getattr(RadiiMotors, attribute)) and not attribute.startswith('__')]
# print(method_list)

with open("/home/pi/projects/log.txt", "a") as file:
    file.write("Creating RadiiMotors object")

radius_motors = RadiiMotors()

with open("/home/pi/projects/log.txt", "a") as file:
    file.write("Finished passing through RadiiMotors' constructor")
    file.write("Starting up RadiusClient")

client = RadiusClient("172.17.21.2")

with open("/home/pi/projects/log.txt", "a") as file:
    file.write("Connected to ThetaServer")

try:
    while True:
        info_received = client.receive_from_theta_server()  # Grab info sent from server

        if isinstance(info_received, dict):
            info_type = list(info_received.keys())[0]
            if info_type == "method":
                print("call a method")
                getattr(radius_motors, info_received[info_type])()
                print("method called!")
                client.send_to_theta_server("Finished homing")
            elif info_type == "point (set_pos)":
                # info_received[info_type] has the format [Rn, Position]
                r_num, pos = info_received[info_type]
                getattr(radius_motors, r_num).set_pos(pos)
            elif info_type == "set_pos_filter":
                # info_received[info_type] has the format [(r1, pos1, bandwidth1), (r1, pos1, bandwidth2)]
                if len(info_received[info_type]) == 2:
                    r1_data, r2_data = info_received[info_type]
                    r1_num, r1_pos, r1_bandwidth = r1_data
                    r2_num, r2_pos, r2_bandwidth = r2_data
                    print("r1_bandwidth:", r1_bandwidth)
                    getattr(radius_motors, r1_num).set_pos_filter(r1_pos, r1_bandwidth)
                    getattr(radius_motors, r2_num).set_pos_filter(r2_pos, r2_bandwidth)
                    # time.sleep(.005) Not sure if I need this???
                elif len(info_received[info_type]) == 1:
                    r_num, r_pos, r_bandwidth = info_received[info_type][0]
                    getattr(radius_motors, r_num).set_pos_filter(r_pos, r_bandwidth)

                client.send_to_theta_server("Finished writing this point")


        elif isinstance(info_received, str):
            if info_received == client.packet_transfer_completed_message:
                radius_motors.r1.idle()
                radius_motors.r2.idle()
                ODrive_Ease_Lib.dump_errors(radius_motors.radius_board)
                radius_motors.r1.clear_errors()
                radius_motors.r2.clear_errors()
            elif info_received == client.close_connection_message:
                break
finally:
    radius_motors.r1.idle()
    radius_motors.r2.idle()
    ODrive_Ease_Lib.dump_errors(radius_motors.radius_board)
    radius_motors.r1.clear_errors()
    radius_motors.r2.clear_errors()
    client.close_connection()
    print("Client closed")

