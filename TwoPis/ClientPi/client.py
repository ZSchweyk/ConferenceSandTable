import enum
import pickle
sys.path.append("~/projects/ConferenceSandTable/TwoPis")
from client_class import Client


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


class RadiusClient:
    def __init__(self):
        #         |Bind IP       |Port |Packet enum
        self.c = Client("172.17.21.1", 5001, PacketType)
        self.c.connect()
        self.is_listening = False
        self.packet_transfer_completed_message = "Complete"

    def start_listening(self):
        self.is_listening = True
        while self.is_listening:
            info_received = self.receive_from_theta_server()
            self.send_to_theta_server(info_received)
            if info_received == "Complete":
                self.is_listening = False
            # Process info_received

    def send_to_theta_server(self, info):
        self.c.send_packet(PacketType.COMMAND1, pickle.dumps(info))

    def receive_from_theta_server(self):
        return pickle.loads(self.c.recv_packet()[1])

    def close_connection(self):
        self.c.close_connection()


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
