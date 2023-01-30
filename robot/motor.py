import RPi.GPIO as GPIO
import time
from enum import Enum

DRIVE_TICKS = 0.25

# GPIO Layout
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

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

        # Drive loop
        drive_ticks = 0
        pwm.start(speed)
        pwm.ChangeDutyCycle(speed)
        while(drive_ticks < ticks+self.encoder_ticks):
            print("Driving " + str(drive_ticks))
            #TODO Need to change this to encoder ticks
            drive_ticks += 1 
            time.sleep(DRIVE_TICKS)
        
        # Stop
        pwm.stop()
        self.stop()


#left_motor = Motor(2, 3, 4, 17)
 right_motor = Motor(19, 26, 21, 20)

#left_motor.drive(Direction.FORWARD, 100, 10)
#left_motor.drive(Direction.REVERSE, 100, 10)

 right_motor.drive(Direction.FORWARD, 100, 10)

 counter = 10
 
Enc_A = 14  
Enc_B = 15
 
def init():
    print "Rotary Encoder Test Program"
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Enc_A, GPIO.IN)
    GPIO.setup(Enc_B, GPIO.IN)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=10)
    return
 
 
def rotation_decode(Enc_A):
    global counter
    sleep(0.002)
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)
 
    if (Switch_A == 1) and (Switch_B == 0):
        counter += 1
        print "direction -> ", counter
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return
 
    elif (Switch_A == 1) and (Switch_B == 1):
        counter -= 1
        print "direction <- ", counter
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return
    else:
        return
 
def main():
    try:
        init()
        while True :
            sleep(1)
 
    except KeyboardInterrupt:
        GPIO.cleanup()