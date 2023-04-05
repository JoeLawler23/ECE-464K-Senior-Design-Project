import sys
import socket
import selectors
import types
import json
import hardware_init as hardware_init
import threading
import time
from multiprocessing import Process
# import pygame

# IPs
# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
HOST = "100.107.15.32"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# def play_audio():
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pass

def test_1():
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 40) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.turn(hardware_init.Direction.COUNTER_CLOCKWISE, 100, 180) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 55) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.turn(hardware_init.Direction.CLOCKWISE, 100, 180) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 40) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    print("SUCCESS")

def test_2():
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 20) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.drive(hardware_init.Direction.REVERSE, 100, 20) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    print("SUCCESS")

def test_3():
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 20) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.turn(hardware_init.Direction.CLOCKWISE, 100, 90) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 20) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.turn(hardware_init.Direction.COUNTER_CLOCKWISE, 100, 90) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    if (robot.drive(hardware_init.Direction.FORWARD, 100, 20) != hardware_init.returnState.SUCCESS):
        print("STOPPED")
        # play_audio()
        return
    time.sleep(0.5)
    print("SUCCESS")

def test_4():
    while(True):
        if (robot.drive(hardware_init.Direction.FORWARD, 100, 50) != hardware_init.returnState.SUCCESS):
            print("STOPPED")
            # play_audio()
            return
        time.sleep(0.5)
        if (robot.drive(hardware_init.Direction.REVERSE, 100, 50) != hardware_init.returnState.SUCCESS):
            print("STOPPED")
            # play_audio()
            return
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
        
#         print(data)

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

#             #TODO turn into Log statement
#             print(f"Drive command received: Direction:{direction}, Distance:{distance}, Speed:{speed}",)

#             # Drive
#             response = robot.drive(direction, speed, distance)

#             # Send response
#             response = {"RESPONSE" : response.value}
#             pi.sendall(bytes(json.dumps(response), encoding = 'utf8'))         

#         elif(command["COMMAND_TYPE"] == "TURN"):
#             # TURN
#             # Heading - 0-360
#             # Speed - 0-100
#             # Direction - LEFT,RIGHT
#             degrees = command["DEGREES"]
#             speed = command["SPEED"]
#             direction = hardware_init.Direction(command["DIRECTION"])

#             # Calculate distance based on heading
#             response = robot.turn(direction, speed, degrees)
            
#             # TODO turn into log statement
#             print(f"Turn command received: Direction:{direction}, Degrees:{degrees}, Speed:{speed}",)
            
#             response = {"RESPONSE" : response.value}
#             pi.sendall(bytes(json.dumps(response), encoding = 'utf8'))  
#         elif(command["COMMAND_TYPE"] == "STOP"):
#             # STOP
#             # No args
#             robot.stop()
#             break
#             #TODO add response type

# TEST CODE HERE
# Init robot
# pygame.init()
# pygame.mixer.init()    
# wav_file = "iphone_alarm.wav"
# pygame.mixer.music.load(wav_file)
left_motor = hardware_init.Motor(2, 3, 4, 17, 14, 15)
right_motor = hardware_init.Motor(19, 26, 20, 21, 5, 6)
left_limit_switch = hardware_init.LimitSwitch(9, 11)
right_limit_switch = hardware_init.LimitSwitch(7, 8)
kinect = hardware_init.Kinect()
robot = hardware_init.Robot(left_motor, right_motor, kinect, left_limit_switch, right_limit_switch)
# robot.init_plots()
# plots = Process(target = robot.update_plots)
# plots.start()

# Get the command-line argument and convert it to an integer
try:
    arg = int(sys.argv[1])
except IndexError:
    print("Error: argument not provided")
    sys.exit()
except ValueError:
    print("Error: argument must be an integer")
    sys.exit()

# Check if the argument is within the valid range and call the appropriate function
if arg == 1:
    test_1()
elif arg == 2:
    test_2()
elif arg == 3:
    test_3()
elif arg == 4:
    test_4()
else:
    print("Error: argument must be between 1 and 3")
