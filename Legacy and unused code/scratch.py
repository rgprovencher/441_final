import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import KICKBOT as kickbot

from TWITBOT import Twitbot

tbot = Twitbot()
print("First run:\n")

if(tbot.updateLastMention()):
    user_name = tbot.lastMention[1]
    tweet_handle = tbot.lastMention[2]
    location = tbot.lastMention[3]
    
    print(user_name)
    print(tweet_handle)
    print(location)
    
else:
    print("no new mentions")
    

print("\nSecond run:\n")

if(tbot.updateLastMention()):
    user_name = tbot.lastMention[1]
    tweet_handle = tbot.lastMention[2]
    location = tbot.lastMention[3]
    
    print(user_name)
    print(tweet_handle)
    print(location)

else:
    print("no new mentions")




#kickbot.kick(1)



GPIO.cleanup()