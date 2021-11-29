from STEP import Stepper
from US_SENSOR import US
from PCF8591 import PCF8591
from SERVO import Servo

import LCD1602

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


# pins and i2c addresses
TEST_LED = 26
PCF_i2c = 0x48
US_TRIG = 16
US_ECHO = 20
LCD_i2c = 0x27
SERVO_PIN = 13
STEP1 = 18
STEP2 = 23
STEP3 = 24
STEP4 = 25
LCD1602.init(0x27, 1)


# SETUP

LCD1602.clear()
GPIO.setup(TEST_LED, GPIO.OUT)

pcf = PCF8591(PCF_i2c)
step = Stepper(STEP1, STEP2, STEP3, STEP4)
us = US(US_TRIG, US_ECHO)
servo = Servo(SERVO_PIN)


timer = time.time()+10
goal = False






time.sleep(1)

# stepper extends servo 
step.goTo(2)

time.sleep(1)

# servo kicks
servo.kick()

# shows me that sensors are running
GPIO.output(TEST_LED, 1)

# reads sensors for 10 seconds, registers a goal
# if something passes the US sensor
while (time.time()<timer):
    
    if (us.read() < 100):
        goal = True
        break
    
    time.sleep(0.1)

# turns off test led, shows sensors aren't reading anymore
GPIO.output(TEST_LED, 0)


# displays goal or no goal on the LCD
if(goal):
    LCD1602.write(4,0, "goooaal")
else:
    LCD1602.write(4,0, "no goal :(")


# step motor returns servo to original position    
step.goTo(0)

# pause
time.sleep(8)

# cleans up
LCD1602.clear()
GPIO.cleanup()
print("done and cleaned up")

