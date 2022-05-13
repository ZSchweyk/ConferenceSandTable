import time
from server import ThetaServer

server = ThetaServer("172.17.21.1")
time.sleep(5)

for i in range(10000):
    server.send_to_radius_client(i)

server.send_to_radius_client("Stop Listening")

server.close_server()
print("Server closed")

