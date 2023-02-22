import sys
import socket
import selectors
import types
import json
import hardware_init as hardware_init
import threading
import time

# IPs
# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
HOST = "100.107.15.32"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# Init motors
# TODO make sure forward is forward for both sides
left_motor = hardware_init.Motor(2, 3, 4, 17, 14, 15)
right_motor = hardware_init.Motor(19, 26, 20, 21, 5, 6)
robot = hardware_init.Robot(left_motor, right_motor)
robot.drive(hardware_init.Direction.FORWARD, 100, 0.25)
time.sleep(0.5)
robot.drive(hardware_init.Direction.REVERSE, 100, 0.25)
time.sleep(0.5)
robot.turn(hardware_init.Direction.CLOCKWISE, 100, 90)
time.sleep(0.5)
robot.drive(hardware_init.Direction.FORWARD, 100, 0.25)
time.sleep(0.5)
robot.drive(hardware_init.Direction.REVERSE, 100, 0.25)
time.sleep(0.5)
robot.turn(hardware_init.Direction.COUNTER_CLOCKWISE, 100, 90)
time.sleep(0.5)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pi:

#     # Init connection
#     connected = False

#     # Attempt to connect to server
#     while not connected:
#         try:
#             pi.connect((HOST, PORT))
#             connected = True
#         except:
#             connected = False

#     # Connected to server
#     while True:

#         # Receive data
#         data = pi.recv(1024)

#         # Load in data
#         command = json.loads(data)

#         # Command structure
#         # COMMAND_TYPE - DRIVE,TURN,STOP
#         if (command["COMMAND_TYPE"] == "DRIVE"):
#             # DRIVE
#             # Direction - FORWARD,REVERSE
#             # Distance(cm) - #
#             # Speed - 0-100
#             direction = hardware_init.Direction(command["DIRECTION"])
#             distance = command["DISTANCE"]
#             speed = command["SPEED"]
#             print(f"Drive command received: Direction:{direction}, Distance:{distance}, Speed:{speed}",)

#             # Drive
#             robot.drive(direction, speed, distance)
            

#         elif(command["COMMAND_TYPE"] == "TURN"):
#             # TURN
#             # Heading - 0-360
#             # Speed - 0-100
#             # Direction - LEFT,RIGHT
#             heading = command["HEADING"]
#             speed = command["SPEED"]
#             direction = hardware_init.Direction[command["DIRECTION"]]

#             # Calculate distance based on heading
#             # TODO
#             distance = 0

#             # Turn left or right
#             if(direction == "LEFT"):
#                 # TODO 
#                 pass
#             elif(direction == "RIGHT"):
#                 # TODO
#                 pass

#         elif(command["COMMAND_TYPE"] == "STOP"):
#             # STOP
#             # No args
#             robot.stop()

#         # Send back
#         # Hits something
#         # Stops
#         # Kinect


#print(f"Received {data!r}")
#sel = selectors.DefaultSelector()
#messages = [b"Message 1 from client.", b"Message 2 from client."]
#start_connections(HOST, PORT, 2)
#print("made it here")
