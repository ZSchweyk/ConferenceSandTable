import enum
import pickle
import sys
sys.path.append("~/projects/ConferenceSandTable/TwoPis")
from server_class import Server


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


class ThetaServer:
    def __init__(self):
        #         |Bind IP       |Port |Packet enum
        self.s = Server("172.17.21.1", 5001, PacketType)
        self.s.open_server()
        self.s.wait_for_connection()

    def send_to_radius_client(self, info):
        self.s.send_packet(PacketType.COMMAND2, pickle.dumps(info))
        assert pickle.loads(self.s.recv_packet()[1]) == info, "Could not send packet"

    def close_server(self):
        self.s.close_connection()
        self.s.close_server()
        print("Server has been stopped")
















