import time

from radii_motors_class import RadiiMotors
from client import RadiusClient

# method_list = [attribute for attribute in dir(RadiiMotors) if callable(getattr(RadiiMotors, attribute)) and not attribute.startswith('__')]
# print(method_list)

# radius_motors = RadiiMotors()

client = RadiusClient("172.17.21.1")

for i in range(10000):
    print(client.receive_from_theta_server())

# while True:
#     info_received = client.receive_from_theta_server()  # Grab info sent from server
#     client.send_to_theta_server(info_received)  # Send it back to confirm that it was received properly
#
#     if isinstance(info_received, dict):
#         info_type = list(info_received.keys())[0]
#         print(info_received[info_type])
#         if info_type == "method":
#             # getattr(radius_motors, info_received[info_type])(args)
#             print("call a method")
#         elif info_type == "point":
#             # info_received[info_type] has the format [Rn, Position]
#             print("go to point")
#         elif info_type == "points":
#             # info_received[info_type] has the format [(r1, pos1), (r1, pos1)]
#             print("go to points")
#
#     elif isinstance(info_received, str):
#         if info_received == client.packet_transfer_completed_message:
#             while client.receive_from_theta_server() != "Stop Listening":
#                 pass
#         elif info_received == client.close_connection_message:
#             client.close_connection()
#             print("Client closed")
#             break

