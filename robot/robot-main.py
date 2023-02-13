import sys
import socket
import selectors
import types
import json
import motor as motor
import threading

# IPs
# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
HOST = "100.107.15.32"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# Init motors
# TODO make sure forward is forward for both sides
left_motor = motor.Motor(2, 3, 4, 17, 14, 15)
right_motor = motor.Motor(19, 26, 21, 20, 5, 6)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as robot:

    # Init connection
    connected = False

    # Attempt to connect to server
    while not connected:
        try:
            robot.connect((HOST, PORT))
            connected = True
        except:
            connected = False

    # Connected to server
    while True:

        # Receive data
        data = robot.recv(1024)

        # Load in data
        command = json.loads(data)

        # Command structure
        # COMMAND_TYPE - DRIVE,TURN,STOP
        if (command["COMMAND_TYPE"] == "DRIVE"):
            # DRIVE
            # Direction - FORWARD,REVERSE
            # Distance(cm) - #
            # Speed - 0-100
            direction = command["DIRECTION"]
            distance = command["DISTANCE"]
            speed = command["SPEED"]

            # TODO MAKE THREAD
            leftMotor = threading(target = left_motor.drive, args = (direction, speed, distance))
            rightMotor = threading(target = right_motor.drive, args = (direction, speed, distance))
            leftMotor.start()
            rightMotor.start()
            leftMotor.join()
            rightMotor.join()

        elif(command["COMMAND_TYPE"] == "TURN"):
            # TURN
            # Heading - 0-360
            # Speed - 0-100
            # Direction - LEFT,RIGHT
            heading = command["HEADING"]
            speed = command["SPEED"]
            direction = command["DIRECTION"]

            # Calculate distance based on heading
            # TODO
            distance = 0

            # Turn left or right
            if(direction == "LEFT"):
                # TODO MAKE THREAD
                leftMotor = threading(target = left_motor.drive, args = ("REVERSE", speed, heading))
                rightMotor = threading(target = right_motor.drive, args = ("FORWARD", speed, heading))
                leftMotor.start()
                rightMotor.start()
                leftMotor.join()
                rightMotor.join()
            elif(direction == "RIGHT"):
                # TODO MAKE THREAD
                leftMotor = threading(target = left_motor.drive, args = ("FORWARD", speed, heading))
                rightMotor = threading(target = right_motor.drive, args = ("REVERSE", speed, heading))
                leftMotor.start()
                rightMotor.start()
                leftMotor.join()
                rightMotor.join()

        elif(command["COMMAND_TYPE"] == "STOP"):
            # STOP
            # No args
            left_motor.stop()
            right_motor.stop()

        # Send back
        # Hits something
        # Stops
        # Kinect


#print(f"Received {data!r}")
#sel = selectors.DefaultSelector()
#messages = [b"Message 1 from client.", b"Message 2 from client."]
#start_connections(HOST, PORT, 2)
#print("made it here")
