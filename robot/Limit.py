import RPi.GPIO as GPIO
import time
from enum import Enum

class Limit_Switch:

    def __init__(self, lims_pin: int, limnc_pin: int)
        """
        Initializes limit switch signals

        Args:
            lims_pin(int): Limit switch signal
            limnc_pin(int): Limit switch no_connect
        """

        #Limit Switch Pins
        self.lims_pin = lims_pin
        self.limnc_pin = limnc_pin
        #set up limit switch
        GPIO.setup(self.lims_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.limnc_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        

        while(1):
            #Limit Switch emergency stop loop
            if(self.lims_pin):
                print("Emergency Stop!")
                #motor.stop
            
            time.sleep(0.01)