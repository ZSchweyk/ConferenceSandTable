import time

from radii_motors_class import RadiiMotors
from client import RadiusClient

# method_list = [attribute for attribute in dir(RadiiMotors) if callable(getattr(RadiiMotors, attribute)) and not attribute.startswith('__')]
# print(method_list)

radius_motors = RadiiMotors()

client = RadiusClient("172.17.21.2")

try:
    while True:
        info_received = client.receive_from_theta_server()  # Grab info sent from server
        client.send_to_theta_server(info_received)  # Send it back to confirm that it was received properly

        if isinstance(info_received, dict):
            info_type = list(info_received.keys())[0]
            print(info_received[info_type])
            if info_type == "method":
                print("call a method")
                getattr(radius_motors, info_received[info_type])()
                print("method called!")
                client.send_to_theta_server("Finished homing")
            elif info_type == "point":
                # info_received[info_type] has the format [Rn, Position]
                print("go to point")
            elif info_type == "points":
                # info_received[info_type] has the format [(r1, pos1), (r1, pos1)]
                print(info_received[info_type])
                r1_data, r2_data = info_received[info_type]
                r1_pos, r1_bandwidth = r1_data[1:3]
                r2_pos, r2_bandwidth = r2_data[1:3]
                radius_motors.r1.set_pos_filter(r1_pos, r1_bandwidth)
                radius_motors.r2.set_pos_filter(r2_pos, r2_bandwidth)

        elif isinstance(info_received, str):
            if info_received == "test packet":
                client.send_to_theta_server("test packet")
            elif info_received == client.close_connection_message:
                break
finally:
    client.close_connection()

