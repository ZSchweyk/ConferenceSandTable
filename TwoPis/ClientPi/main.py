import sys
sys.path.append("~/projects/ConferenceSandTable/TwoPis")
from client import RadiusClient



c = RadiusClient()
is_running = True
while is_running:
    is_running = c.start_listening()

print("Client finished running")