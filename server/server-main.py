import sys, termios, tty, os
import socket
import selectors
import types
import keyboard
import json
import threading
import signal
import time
import multiprocessing
from enum import Enum
sel = selectors.DefaultSelector()


class Direction(Enum): 
    FORWARD = 1
    REVERSE = 2
# ...
# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
# Robot-2 is the server and Robot-1 is the client **server is offline in this demo**
HOST = "100.107.15.32"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

portsInUse = []
threads = []
mySocket = 0

 
def handler(signum, frame): #for CTRL-C for reboot
    mySocket.shutdown()
    for i in threads:
        mySocket.close()
    sys.exit()

def getch(): #not necessary, just used for testing
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def myThread(conn, addr, s, port):
    with conn:
        print(f"Connected by {addr}")
        while True:
            char = getch()
            if char == "a":
                x = {"COMMAND_TYPE" : "TURN", #DRIVE, TURN, STOP
                    "HEADING": 20,
                    "SPEED": 80,
                    "DIRECTION": "LEFT",
                    "DISTANCE": None}
                conn.sendall(bytes(json.dumps(x), encoding = 'utf8'))
            elif char == "d":
                x = {"COMMAND_TYPE" : "TURN", #DRIVE, TURN, STOP
                    "HEADING": 20, 
                    "SPEED": 80,
                    "DIRECTION": "RIGHT",
                    "DISTANCE": None}
                conn.sendall(bytes(json.dumps(x), encoding = 'utf8'))
            elif char == "w":
                x = {"COMMAND_TYPE" : "DRIVE", #DRIVE, TURN, STOP
                    "HEADING": None, 
                    "SPEED": 80,
                    "DIRECTION": "FORWARD",
                    "DISTANCE": 50}
                conn.sendall(bytes(json.dumps(x), encoding = 'utf8'))
            elif char == "s":
                x = {"COMMAND_TYPE" : "DRIVE", #DRIVE, TURN, STOP
                    "HEADING": None, 
                    "SPEED": 80,
                    "DIRECTION": "BACKWARD",
                    "DISTANCE": 50}
                conn.sendall(bytes(json.dumps(x), encoding = 'utf8'))
            elif char == "q":
                x = {"COMMAND_TYPE": "STOP"}
                conn.sendall(bytes(json.dumps(x), encoding = 'utf8'))
                break
            else:
                print(char)



signal.signal(signal.SIGINT, handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    mySocket = s
    while True:
        s.listen()
        conn, addr = s.accept()
        thisThread = threading.Thread(target = myThread, args = (conn, addr, s, PORT))
        thisThread.daemon = True
        thisThread.start()
        threads.append(thisThread)
for i in threads:
    i.join()
s.shutdown()
s.close()

        