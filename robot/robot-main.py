import sys
import socket
import selectors
import types
import json
import motor.py as motor
#import motor
# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
# Robot-2 is the server and Robot-1 is the client **server is offline in this demo**
HOST = "100.107.15.32"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

left_motor = Motor(2, 3, 4, 17, 14, 15)
right_motor = Motor(19, 26, 21, 20, 5, 6)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    connected = False
    while not connected:
        try:
            s.connect((HOST, PORT))
            connected = True
        except:
            connected = False
    while True:
        data = s.recv(1024)
        if data == b"quit":
            left_motor.stop()
            right_motor.stop()
            break
        y = json.loads(data)

        # Drive - (Destination (x,y,h), Speed)
        # Turn - (h, Speed)

        # Send back
        # Hits something
        # Stops
        # Kinect

        left_motor.drive(y["direction"], 100, 10)
        right_motor.drive(y["direction"], 100, 10)
        print(y["direction"])


#print(f"Received {data!r}")
#sel = selectors.DefaultSelector()
#messages = [b"Message 1 from client.", b"Message 2 from client."]
#start_connections(HOST, PORT, 2)
#print("made it here")
