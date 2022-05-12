import enum
import pickle
from client_class import Client


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


#         |Server IP     |Port |Packet enum
c = Client("172.17.21.1", 5001, PacketType)
c.connect()

while True:
    val_from_server = pickle.loads(c.recv_packet()[1])
    if val_from_server == "Complete":
        break
    print(val_from_server)
    c.send_packet(PacketType.COMMAND1, pickle.dumps("Received"))


c.close_connection()
