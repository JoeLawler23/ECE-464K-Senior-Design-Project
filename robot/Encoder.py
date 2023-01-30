import RPi.GPIO as GPIO
import time


#calling format func
#def my_function():
  #print("Hello from a function")
# GPIO Layout
def GPIO_OUTPUT(motor, speed, direction):


GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

# Motor Driver Pin Definitions Motor 1
L_EN = 2; # Reverse/Enable (Active HIGH)
R_EN = 3; # Forward/Enable (Active HIGH)
LPWM = 4; # Reverse/PWM (Active HIGH)
RPWM = 17; # Forward/PWM (Active HIGH)

# Motor Driver Pin Definitions Motor 2
L_EN2 = 2; # Reverse/Enable (Active HIGH)
R_EN2 = 3; # Forward/Enable (Active HIGH)
LPWM2 = 4; # Reverse/PWM (Active HIGH)
RPWM2 = 17; # Forward/PWM (Active HIGH)


# Set all of our PINS to output

GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(F_EN, GPIO.OUT)
GPIO.setup(FPWM, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)


# Drive the motors forward
GPIO.output(F_EN, True)

# Setup PWM on right motor
pwm1 = GPIO.PWM(FPWM, 100)
pwm1.ChangeDutyCycle(0)
pwm1.start(0)

# Infinite Loop
while 1:

    # Increase duty cycle
    for x in range(100):
        print("Speeding up " + str(x))
        pwm1.ChangeDutyCycle(x)
        time.sleep(0.25)

    # Sleep for 5 seconds
    time.sleep(5)

    # Decrease duty cycle
    for x in range(100):
        print("Slowing down " + str(x))
        pwm1.ChangeDutyCycle(100-x)
        time.sleep(0.25)


        counter = 10
 
Enc_A = 17  
Enc_B = 27  
 
 
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