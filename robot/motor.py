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

    def __init__(self, ren_pin, fen_pin, rpwm_pin, fpwm_pin, encodera, encoderb):
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
        self.encoder_pina = encodera
        self.encoder_pinb = encoderb
        self.encoder_ticks = 0
        #encoder pins
        
        GPIO.setup(self.encoder_pinb, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoder_pina, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(self.encoder_pina, GPIO.RISING, callback=rotation_decode, bouncetime=10)
        #GPIO.add_event_detect(self.encoder_pinb, GPIO.RISING, callback=rotation_decode, bouncetime=10)

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
        clklaststate = GPIO.input(self.encoder_pina)
        printclk = 1
        pwm.start(speed)
        pwm.ChangeDutyCycle(speed)
        # while(printclk):
        #     print("Driving " + str(drive_ticks))
        #     time.sleep(DRIVE_TICKS)
        while(drive_ticks < ticks+self.encoder_ticks):
            print("Driving " + str(drive_ticks))
            
            
            #TODO Need to change this to encoder ticks
            clkState = GPIO.input(self.encoder_pina)
            dtState = GPIO.input(self.encoder_pinb)
            if clkState != clklaststate:
                # if dtState != clkState:
                #     drive_ticks += 1
                # else:
                #     drive_ticks -= 1
                drive_ticks += 1
                
            clklaststate = clkState
            time.sleep(0.01)
            # if (Switch_A == 1) and (Switch_B == 0):
            #     drive_ticks += 1
            #     print ("direction -> ", drive_ticks)
            #     if Switch_B == 0:
            #         Switch_B = GPIO.input(self.encoder_pinb)
            #     if Switch_B == 1:
            #         Switch_B = GPIO.input(self.encoder_pinb)
                
 
            # elif (Switch_A == 1) and (Switch_B == 1):
            #     drive_ticks -= 1
            #     print ("direction <- ", drive_ticks)
            #     if Switch_A == 1:
            #         Switch_A = GPIO.input(self.encoder_pina)

            # #drive_ticks += 1 
            # time.sleep(0.025)

        
        # Stop
        pwm.stop()
        self.stop()

left_motor = Motor(2, 3, 4, 17, 14, 15)
#right_motor = Motor(19, 26, 21, 20, 5, 6)
#28 ticks should be one rotation of the wheel but there is a decent amount of leeway when we were testing
left_motor.drive(Direction.FORWARD, 100, 40)
#left_motor.drive(Direction.REVERSE, 100, 40)

#right_motor.drive(Direction.FORWARD, 100, 10)
#############################################################
#counter = 10
 
# Enc_A = 14  
# Enc_B = 15
 
# def init():
#     print ("Rotary Encoder Test Program")
#     GPIO.setwarnings(True)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(Enc_A, GPIO.IN)
#     GPIO.setup(Enc_B, GPIO.IN)
#     GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=10)
#     return
 
 
# def rotation_decode(Enc_A):
#     global counter
#     sleep(0.002)
#     Switch_A = GPIO.input(Enc_A)
#     Switch_B = GPIO.input(Enc_B)
 
#     if (Switch_A == 1) and (Switch_B == 0):
#         counter += 1
#         print ("direction -> ", counter)
#         while Switch_B == 0:
#             Switch_B = GPIO.input(Enc_B)
#         while Switch_B == 1:
#             Switch_B = GPIO.input(Enc_B)
        
 
#     elif (Switch_A == 1) and (Switch_B == 1):
#         counter -= 1
#         print ("direction <- ", counter)
#         while Switch_A == 1:
#             Switch_A = GPIO.input(Enc_A)
#         return
#     else:
#         return
 
# def main():
#     try:
#         init()
#         while True :
#             sleep(1)
 
#     except KeyboardInterrupt:
#         GPIO.cleanup()