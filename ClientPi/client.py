import enum
import pickle
from client_class import Client
from logging_func import LOG


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


class RadiusClient:
    def __init__(self, server_ip_address):
        #         |Bind IP       |Port |Packet enum
        self.c = Client(server_ip_address, 5001, PacketType)
        while True:
            try:
                LOG("Trying to connect to server")
                self.c.connect()
                break
            except:
                pass
        self.is_listening = False
        self.packet_transfer_completed_message = "Finished Drawing Equation"
        self.close_connection_message = "Disconnect"

    def start_listening(self):
        self.is_listening = True
        while self.is_listening:
            info_received = self.receive_from_theta_server()  # Grab info sent from server
            self.send_to_theta_server(info_received)  # Send it back to confirm that it was received properly
            if info_received == self.packet_transfer_completed_message:
                self.is_listening = False
                return False
            if info_received == self.close_connection_message:
                self.close_connection()
                return False  # Stop the main while True loop outside of this class
            # Process info_received
            yield info_received
        # return True  # Keep the main while True loop outside of this class going

    def send_to_theta_server(self, info):
        self.c.send_packet(PacketType.COMMAND1, pickle.dumps(info))

    def receive_from_theta_server(self):
        val_to_return = pickle.loads(self.c.recv_packet()[1])
        # self.send_to_theta_server(val_to_return)
        return val_to_return

    def close_connection(self):
        self.c.close_connection()





