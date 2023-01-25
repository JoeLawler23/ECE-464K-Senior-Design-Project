import RPi.GPIO as GPIO
import time
from enum import Enum

DRIVE_TICKS = 0.25

class Direction(Enum): 
    FORWARD = 1
    REVERSE = 2

class Motor:

    def __init__(self, ren_pin, fen_pin, rpwm_pin, fpwm_pin):
        # Assign pins
        self.ren_pin = ren_pin # Reverse/Enable (Active HIGH)
        self.fen_pin = fen_pin # Forward/Enable (Active HIGH)
        self.rpwm_pin = rpwm_pin # Reverse/PWM (Active HIGH)
        self.fpwm_pin = fpwm_pin # Forward/PWM (Active HIGH)

        # Set all of our PINS to output
        GPIO.setup(self.ren_pin, GPIO.OUT)
        GPIO.setup(self.fen_pin, GPIO.OUT)
        GPIO.setup(self.rpwm_pin, GPIO.OUT)
        GPIO.setup(self.fpwm_pin, GPIO.OUT)

        # Encoder init
        self.encoder_ticks = 0

    def stop(self):
        GPIO.output(self.ren_pin, False)
        GPIO.output(self.fen_pin, False)

    def drive(self, direction: Direction, speed: int, ticks: int):

        # Init pwm
        pwm = None

        # Set direction & Setup PWM
        if (direction == Direction.FORWARD):
            # Enable pins
            GPIO.output(self.fen_pin, True)
            GPIO.output(self.ren_pin, False)

            # Setup PWM
            pwm = GPIO.PWM(self.fpwm_pin, speed)

        elif (direction == Direction.REVERSE):
            # Enable pins
            GPIO.output(self.ren_pin, True)
            GPIO.output(self.fen_pin, False)

            # Setup PWM
            pwm = GPIO.PWM(self.rpwm_pin, speed)
        else:
            print("Invalid direction")
            return

        # Drive loop
        drive_ticks = 0
        pwm.start(speed)
        while(drive_ticks < ticks+self.encoder_ticks):
            print("Driving " + str(drive_ticks))
            #TODO Need to change this to encoder ticks
            drive_ticks += 1 
            time.sleep(DRIVE_TICKS)
        
        # Stop
        pwm.stop()
        self.stop()


left_motor = Motor(2, 3, 4, 17)
right_motor = Motor(19, 26, 21, 20)

left_motor.drive(Direction.FORWARD, 100, 10)
right_motor.drive(Direction.FORWARD, 100, 10)
