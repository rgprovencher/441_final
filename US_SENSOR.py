# class object to control ultrasonic sensors.

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



class US:
    
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        
    # sends a 10us "on" signal to trig pin
    def __trigger(self):
        # define a 10us burst time
        pulse_time = time.time() + float(10/1e6)
        
        GPIO.output(self.trig, 1)
        
        while time.time() < pulse_time:
            pass
        
        GPIO.output(self.trig, 0)
    
    
    # returns distance in cm
    def read(self):
        # sends a pulse
        self.__trigger()
        

        while (GPIO.input(self.echo)==0):
            time_out = time.time()
        while (GPIO.input(self.echo)==1):
            time_in = time.time()
        
  
        # multiply time elapsed by 34300 cm/s, then /2 to account for there-and-back
        dist = (time_in-time_out)*34300 / 2
        
        return dist
        
            
    
    