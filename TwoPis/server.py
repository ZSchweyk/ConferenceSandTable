import enum
import pickle
from server_class import Server


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


#         |Bind IP       |Port |Packet enum
s = Server("192.168.178.1", 5001, PacketType)
s.open_server()
s.wait_for_connection()

s.send_packet(PacketType.COMMAND2, pickle.dumps("Hello from the Server!"))
print(pickle.loads(s.recv_packet()[1]))

s.close_connection()
s.close_server()
