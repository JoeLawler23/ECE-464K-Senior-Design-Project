import RPi.GPIO as GPIO
import time

# GPIO Layout
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

# Motor Driver Pin Definitions
L_EN = 2; # Reverse/Enable (Active HIGH)
R_EN = 3; # Forward/Enable (Active HIGH)
LPWM = 4; # Reverse/PWM (Active HIGH)
RPWM = 17; # Forward/PWM (Active HIGH)

# Set all of our PINS to output
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

# Drive the motors forward
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)

# Setup PWM on right motor
rpwm= GPIO.PWM(RPWM, 100)
rpwm.ChangeDutyCycle(0)
rpwm.start(0)

# Infinite Loop
while 1:

    # Increase duty cycle
    for x in range(100):
        print("Speeding up " + str(x))
        rpwm.ChangeDutyCycle(x)
        time.sleep(0.25)

    # Sleep for 5 seconds
    time.sleep(5)

    # Decrease duty cycle
    for x in range(100):
        print("Slowing down " + str(x))
        rpwm.ChangeDutyCycle(100-x)
        time.sleep(0.25)