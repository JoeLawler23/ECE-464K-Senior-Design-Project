import RPi.GPIO as GPIO
import time
from enum import Enum
import freenect
import matplotlib.pyplot as plt

# GPIO Layout
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

# Constants
# TODO needs to be adjusted
TICKS_PER_CM = 5
TICKS_PER_DEGREE = 10

# Direction Enum
class Direction(Enum): 
    FORWARD = 1
    REVERSE = 2
    CLOCKWISE = 3
    COUNTER_CLOCKWISE = 4

# Return State Enum
class returnState(Enum):
    SUCCESS = 1
    STOP_FAIL = 2
    STOP_SAFETY = 3

# Motor Class
class Motor:

    def __init__(self, ren_pin: int, fen_pin: int, rpwm_pin: int, fpwm_pin: int, etick_pin: int, eref_pin: int):
        """
        Initializes motor controller and encoder for a given motor

        Args:
            ren_pin (int): Reverse/Enable pin 
            fen_pin (int): Forward/Enable pin
            rpwm_pin (int): Reverse/PWM pin 
            fpwm_pin (int): Forward/PWM pin 
            etick_pin (int): Encoder tick pin
            eref_pin (int): Encoder reference pin
        """

        # Assign motor pins
        self.ren_pin = ren_pin # Reverse/Enable (Active HIGH)
        self.fen_pin = fen_pin # Forward/Enable (Active HIGH)
        self.rpwm_pin = rpwm_pin # Reverse/PWM (Active HIGH)
        self.fpwm_pin = fpwm_pin # Forward/PWM (Active HIGH)

        # Set all of our PINS to output
        GPIO.setup(self.ren_pin, GPIO.OUT)
        GPIO.setup(self.fen_pin, GPIO.OUT)
        GPIO.setup(self.rpwm_pin, GPIO.OUT)
        GPIO.setup(self.fpwm_pin, GPIO.OUT)

        # Encoder pins
        self.etick_pin = etick_pin
        self.eref_pin = eref_pin
        self.encoder_ticks = 0

        # Set encoder pins
        GPIO.setup(self.eref_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.etick_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def stop(self):
        """
        Stops motor by turning off forward and reverse pins
        """        
        GPIO.output(self.ren_pin, False)
        GPIO.output(self.fen_pin, False)

class LimitSwitch:

    def __init__(self) -> None:
        pass

class Kinect:

    def __init__(self):
        # self.depth = freenect.sync_get_depth()
        # self.video = freenect.sync_get_video()
        print("KINECT IS SETUP")

    def update_depth(self):
        depth, _ = freenect.sync_get_depth()
        self.depth = depth
        # TODO return whatever distance data desired

    def update_video(self):
        video, _ = freenect.sync_get_video()
        self.video = video

    def stop(self):
        #TODO
        return

class Speaker:

    def __init__(self) -> None:
        pass

class Robot:

    def __init__(self, left_motor: Motor, right_motor: Motor, kinect: Kinect):
        """
        Initializes robot with left and right motors

        Args:
            left_motor (Motor): Left motor
            right_motor (Motor): Right motor
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.kinect = kinect

    def init_plots(self):
        # Init plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
    
    def update_plots(self):
        # Update the subplots in real time
        # while True:
        # Capture a color frame and a depth frame from the Kinect sensor
            
        self.kinect.update_depth()
        self.kinect.update_video()

        depth = self.kinect.depth
        video = self.kinect.video

        # Convert the video data to an RGB image
        rgb_image = video[:, :, ::-1]

        # Display the color image as a subplot
        self.ax1.clear()
        self.ax1.imshow(rgb_image)
        self.ax1.set_title('Color Image')

        # Display the depth map as a subplot
        self.ax2.clear()
        self.ax2.imshow(depth, cmap='gray')
        self.ax2.set_title('Depth Map')

        # Update the subplots with the latest data
        plt.draw()
        plt.pause(0.001)
        print("PLOTS UPDATED")

    def stop(self):
            """
            Stops robot by stopping both motors
            """
            self.left_motor.stop()
            self.right_motor.stop()
    
    def drive(self, direction: Direction, speed: int, distance: int):
        """
        Drives robot forward or reverse a given distance at a given speed

        Args:
            direction (Direction): Direction to drive
            speed (int): Speed to drive at
            distance (int): Distance to drive
        """

        # Clip inputs
        speed = abs(speed)
        distance = abs(distance)
        
        # Init pwm
        left_motor_pwm = None
        right_motor_pwm = None

        # Enable pins
        GPIO.output(self.left_motor.ren_pin, True)
        GPIO.output(self.left_motor.fen_pin, True)
        GPIO.output(self.right_motor.ren_pin, True)
        GPIO.output(self.right_motor.fen_pin, True)

        # Set direction & Setup PWM
        if (direction == Direction.FORWARD):

            # Setup PWM
            left_motor_pwm = GPIO.PWM(self.left_motor.fpwm_pin, speed)
            right_motor_pwm = GPIO.PWM(self.right_motor.fpwm_pin, speed)

        elif (direction == Direction.REVERSE):

            # Setup PWM
            left_motor_pwm = GPIO.PWM(self.left_motor.rpwm_pin, speed)
            right_motor_pwm = GPIO.PWM(self.right_motor.rpwm_pin, speed)

        else:
            print("Invalid direction")
            return returnState.STOP_FAIL
        
        # Calculate ticks from distance
        destination_ticks = int(distance * TICKS_PER_CM)

        # Init vars for driving
        left_clklaststate = GPIO.input(self.left_motor.etick_pin)
        right_clklaststate = GPIO.input(self.right_motor.etick_pin)

        # Start pwm
        left_motor_pwm.start(speed)
        right_motor_pwm.start(speed)
        left_motor_pwm.ChangeDutyCycle(speed)
        right_motor_pwm.ChangeDutyCycle(speed)

        # Average ticks
        left_ticks = 0
        right_ticks = 0
        avg_ticks = 0

        # Drive loop
        # TODO add timeout
        print(f"Driving {direction} {distance} centimeters")
        while (avg_ticks < destination_ticks):

             # Get encoder input
            left_clkState = GPIO.input(self.left_motor.etick_pin)
            right_clkState = GPIO.input(self.right_motor.etick_pin)

            # Increment left ticks if encoder tick
            if left_clkState != left_clklaststate:
                left_ticks += 1
                
            # Increment right ticks if encoder tick
            if right_clkState != right_clklaststate:
                right_ticks += 1
                
            # Update encoder state
            left_clklaststate = left_clkState
            right_clklaststate = right_clkState

            # Calculate encoder average
            avg_ticks = (left_ticks + right_ticks)/2
            
            # Log
            print(f"DRIVE LOOP: average: {avg_ticks}, left: {left_ticks}, right: {right_ticks}, destination: {destination_ticks}")

            # TODO check for any interrupts
            if (False):
                return returnState.STOP_SAFETY 

            # Wait to process
            time.sleep(0.01)

        #TODO If timeout reached
        if (False):
            return returnState.STOP_FAIL

        # Stop motors
        self.stop()

        return returnState.SUCCESS

    def turn(self, direction: Direction, speed: int, degrees: int):
        """
        Drives robot forward or reverse a given distance at a given speed

        Args:
            direction (Direction): Direction to drive
            speed (int): Speed to drive at
            distance (int): Distance to drive
        """

        # Clip inputs
        speed = abs(speed)
        degrees = abs(degrees)
        
        # Init pwm
        left_motor_pwm = None
        right_motor_pwm = None

        # Enable pins
        GPIO.output(self.left_motor.ren_pin, True)
        GPIO.output(self.left_motor.fen_pin, True)
        GPIO.output(self.right_motor.ren_pin, True)
        GPIO.output(self.right_motor.fen_pin, True)

        # Set direction & Setup PWM
        if (direction == Direction.CLOCKWISE):

            # Setup PWM
            left_motor_pwm = GPIO.PWM(self.left_motor.fpwm_pin, speed)
            right_motor_pwm = GPIO.PWM(self.right_motor.rpwm_pin, speed)

        elif (direction == Direction.COUNTER_CLOCKWISE):

            # Setup PWM
            left_motor_pwm = GPIO.PWM(self.left_motor.rpwm_pin, speed)
            right_motor_pwm = GPIO.PWM(self.right_motor.fpwm_pin, speed)

        else:
            print("Invalid direction")
            return returnState.STOP_FAIL
        
        # Calculate ticks from distance
        # TODO calculate this better
        destination_ticks = int(degrees * TICKS_PER_DEGREE)

        # Init vars for driving
        left_clklaststate = GPIO.input(self.left_motor.etick_pin)
        right_clklaststate = GPIO.input(self.right_motor.etick_pin)

        # Start pwm
        left_motor_pwm.start(speed)
        right_motor_pwm.start(speed)
        left_motor_pwm.ChangeDutyCycle(speed)
        right_motor_pwm.ChangeDutyCycle(speed)

        # Average ticks
        left_ticks = 0
        right_ticks = 0
        avg_ticks = 0

        # Drive loop
        # TODO add timeout
        print(f"Turning {direction} {degrees} degrees")
        while (avg_ticks < destination_ticks):

             # Get encoder input
            left_clkState = GPIO.input(self.left_motor.etick_pin)
            right_clkState = GPIO.input(self.right_motor.etick_pin)

            # Increment left ticks if encoder tick
            if left_clkState != left_clklaststate:
                left_ticks += 1
                
            # Increment right ticks if encoder tick
            if right_clkState != right_clklaststate:
                right_ticks += 1
                
            # Update encoder state
            left_clklaststate = left_clkState
            right_clklaststate = right_clkState

            # Calculate encoder average
            avg_ticks = (left_ticks + right_ticks)/2
            
            # Log
            print(f"TURN LOOP: average: {avg_ticks}, left: {left_ticks}, right: {right_ticks}, destination: {destination_ticks}")

            # TODO check for any interrupts
            if (False):
                return returnState.STOP_SAFETY 

        #TODO If timeout reached
        if (False):
            return returnState.STOP_FAIL

        # Stop motors
        self.stop()

        return returnState.SUCCESS
