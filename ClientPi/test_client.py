from client import RadiusClient


client = RadiusClient("localhost")

try:
    while True:
        value = client.receive_from_theta_server()
        if value == "Done":
            break
        print(value)
finally:
    client.close_connection()








# import enum
# from client_class import Client
# import pickle
#
#
# class PacketType(enum.Enum):
#     NULL = 0
#     COMMAND1 = 1
#     COMMAND2 = 2
#
#
# client = Client("localhost", 5001, PacketType)
# client.connect()
#
# try:
#     while True:
#         value = pickle.loads(client.recv_packet()[1])
#         print(value)
#         if value == "Done":
#             break
# finally:
#     client.close_connection()

