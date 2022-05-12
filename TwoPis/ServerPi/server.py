import enum
import pickle
from server_class import Server


class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2


def run_server(equation: str, period, theta_speed=.75, scale_factor=1, sleep=.005):
    #         |Bind IP       |Port |Packet enum
    s = Server("172.17.21.1", 5001, PacketType)
    s.open_server()
    s.wait_for_connection()


    for i in range(1, 101):
        s.send_packet(PacketType.COMMAND2, pickle.dumps(i))
        print(pickle.loads(s.recv_packet()[1]))

    s.send_packet(PacketType.COMMAND2, pickle.dumps("Complete"))

    s.close_connection()
    s.close_server()
