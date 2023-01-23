import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
supply = 1

GPIO.setup(supply,GPIO.OUT)

GPIO.output(supply,GPIO.HIGH)

sleep(2)
//turning off
GPIO.output(supply,GPIO.LOW)

//reset
GPIO.cleanup()

print("Hello")
