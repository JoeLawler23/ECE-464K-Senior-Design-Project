import RPi.GPIO as GPIO
import time
from enum import Enum

# GPIO Layout
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

# Constants
# TODO needs to be adjusted
TICKS_PER_CM = 50



# Direction Enum
class Direction(Enum): 
    FORWARD = 1
    REVERSE = 2

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

    def drive(self, direction: Direction, speed: int, distance: int):
        """
        Drive for a given distance

        Args:
            direction (Direction): Direction to drive in, FORWARD/REVERSE
            speed (int): Speed to drive at (0-100)
            distance (int): Distance in cm to drive (Value must be positive)
        """

        # Clip inputs
        speed = abs(speed)
        distance = abs(distance)
        
        # Init pwm
        pwm = None
        
        # Enable pins
        GPIO.output(self.ren_pin, True)
        GPIO.output(self.fen_pin, True)

        # Set direction & Setup PWM
        if (direction == Direction.FORWARD):

            # Setup PWM
            pwm = GPIO.PWM(self.fpwm_pin, speed)

        elif (direction == Direction.REVERSE):

            # Setup PWM
            pwm = GPIO.PWM(self.rpwm_pin, speed)
        else:
            print("Invalid direction")
            return

        # Calculate ticks from distance
        ticks = int(distance * TICKS_PER_CM)

        # Init vars for driving
        drive_ticks = 0
        clklaststate = GPIO.input(self.etick_pin)

        # Start pwm
        pwm.start(speed)
        pwm.ChangeDutyCycle(speed)

        # Drive loop 
        while(drive_ticks < ticks+self.encoder_ticks):

            # Get encoder input
            clkState = GPIO.input(self.etick_pin)

            # Increment drive ticks if encoder tick
            if clkState != clklaststate:
                drive_ticks += 1
                
            # Update encoder state
            clklaststate = clkState
            

            # Wait to process
            time.sleep(0.01)
        
        # Stop
        pwm.stop()
        self.stop()

    def testMotor(self):
        """
        Test motor by driving forward and reverse
        """
        print("DRIVE MOTOR FORWARD 40cm\n")
        self.drive(Direction.FORWARD, 100, 40)
        print("DRIVE MOTOR BACKWARD 40cm\n")
        self.drive(Direction.REVERSE, 100, 40)