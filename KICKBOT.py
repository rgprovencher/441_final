# class object that controls the mechatronic functions
# of the foosball table. recieves commands from background
# process kickbot_manager.py

from STEP import Stepper
from US_SENSOR import US
from SERVO import Servo
import multiprocessing

import LCD1602

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)



# ultrasonic pins
# (NOTE! Ultrasonic TAKES 5v power but must RETURN 3.3v to the GPIO)
US_TRIG = 13
US_ECHO = 19

# LCD address and initialization
# NOTE! LCD TAKES 3.3v power
LCD_i2c = 0x27
LCD1602.init(0x27, 1)

# servo (kicker) pin
SERVO_PIN = 12

# step motor(s) pins
STEP1 = 18
STEP2 = 23
STEP3 = 24
STEP4 = 25


# global variables
# time between kick and program deciding you missed, if
# no goal registered (in seconds)
SHOT_TIME = 4
# distance threshhold used to determine if
# something has passed in front of the
# ultrasonic sensor
SENSOR_DIST = 10


class Kickbot:
    
    def __init__(self):

        LCD1602.clear()
        
        self.step = Stepper(STEP1, STEP2, STEP3, STEP4)
        self.us = US(US_TRIG, US_ECHO)
        self.servo = Servo(SERVO_PIN)
           
    
    
    # used to manually adjust servo position
    def goLeft(self):
        self.step.halfStep(1)
    def goRight(self):
        self.step.halfStep(-1)
    


    # kick routine: moves servo-driven kicker to specified
    # location, activates a kick command, reads the sensor
    # to determine if a goal has been scored or not, and
    # finally returns whether or not a goal has been scored
    # as a boolean
    def kick(self, distance):
        LCD1602.clear()
        LCD1602.write(4, 0," go go go")
        goal = False

        time.sleep(1)

        # stepper extends servo 
        self.step.goTo(distance)
        
        time.sleep(.5)

        # servo kicks
        self.servo.kick()

        # reads sensors for specified number of seconds, registers a goal
        # if something passes the US sensor
        timer = time.time()+SHOT_TIME
        
        while (time.time()<timer):
            
            if (self.us.read() < SENSOR_DIST):
                goal = True
                break
            
            time.sleep(0.02)

        
        # displays goal or no goal on the LCD
        LCD1602.clear()
        if(goal):
            LCD1602.write(4,0, "goooaal")
        else:
            LCD1602.write(4,0, "no goal :(")


        # returns goal status
        return goal






