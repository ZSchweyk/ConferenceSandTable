import enum
import pickle
from client_class import Client


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


class RadiusClient:
    def __init__(self):
        #         |Bind IP       |Port |Packet enum
        self.c = Client("172.17.21.1", 5001, PacketType)
        while True:
            try:
                self.c.connect()
                break
            except ConnectionRefusedError:
                pass
        self.is_listening = False
        self.packet_transfer_completed_message = "Stop Listening"
        self.close_connection_message = "Close Connection"

    def start_listening(self):
        self.is_listening = True
        while self.is_listening:
            info_received = self.receive_from_theta_server()  # Grab info sent from server
            self.send_to_theta_server(info_received)  # Send it back to confirm that it was received properly
            print("Received " + str(info_received))
            if info_received == self.packet_transfer_completed_message:
                self.is_listening = False
            if info_received == self.close_connection_message:
                self.close_connection()
                return False  # Stop the main while True loop outside of this class
            # Process info_received
        return True  # Keep the main while True loop outside of this class going

    def send_to_theta_server(self, info):
        self.c.send_packet(PacketType.COMMAND1, pickle.dumps(info))

    def receive_from_theta_server(self):
        return pickle.loads(self.c.recv_packet()[1])

    def close_connection(self):
        self.c.close_connection()



c = RadiusClient()
is_running = True
while is_running:
    is_running = c.start_listening()

print("Client finished running")

