from KICKBOT import Kickbot
import json
import multiprocessing
import ctypes
from TWITBOT import Twitbot
import READER as Reader

from STEP import Stepper
from US_SENSOR import US
from PCF8591 import PCF8591
from SERVO import Servo

import LCD1602

from urllib.request import urlopen
from urllib.parse import urlencode

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


KICK_BUTTON = 20
GPIO.setup(KICK_BUTTON, GPIO.IN)

print(Reader.location())
print(Reader.waiting())

# step motor 1 pins
STEP1 = 18
STEP2 = 23
STEP3 = 24
STEP4 = 25

US_TRIG = 13
US_ECHO = 19

LCD_i2c = 0x27
LCD1602.init(0x27, 1)

# servo (kicker) pin
SERVO_PIN = 12

step1 = Stepper(STEP1, STEP2, STEP3, STEP4)
servo = Servo(SERVO_PIN)

us = US(US_TRIG, US_ECHO)



v = multiprocessing.Value(ctypes.c_wchar_p, "tango")


v.value = "apricot"


TWITTER_OVERRIDE = multiprocessing.Array("f", 3)
TWITTER_OVERRIDE[0] = 0 # used as a true/false flag to override html check
TWITTER_OVERRIDE[1] = 0 # stores location extracted from tweets
TWITTER_OVERRIDE[2] = -1 # stores goal status

print(TWITTER_OVERRIDE[2])


# # move steppers
#step1.goTo(2)

# test LCD
#LCD1602.clear()
#LCD1602.write(4, 0, "rob = king")

# #test servo
# servo.kick()
# 

# goal = 1
# 
# TS_api = "C6IAUA69SWYN55O9"
# 
# params = {
#     "api_key":TS_api,
#     1: goal }
# params = urlencode(params)   # put dict data into a GET string

# add "?" to URL and append with parameters in GET string:
# url = "https://api.thingspeak.com/update?" + params

# 
# try:
#     print("speaking")
#     response = urlopen(url)      # open the URL to send the request
#     print(response.status, response.reason)  # display the response
#     print(response.read()) # display response page data
#     time.sleep(16)    # 15 sec minimum
# except Exception as e:
#     print(e)


while 1:
    print(us.read())
    time.sleep(.02)



