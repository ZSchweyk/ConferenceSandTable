import enum
from client_class import Client


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2

#         |Server IP     |Port |Packet enum
c = Client("192.168.178.1", 5001, PacketType)
c.connect()

print(c.recv_packet())
c.send_packet(PacketType.COMMAND1, b"Hello from the Client!")

c.close_connection()

