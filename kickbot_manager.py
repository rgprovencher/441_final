# runs as a background process to control the mechatronic foosball table.
# opens a daemon process to check for input from twitter, while the
# main process checks a user_input file for input from the html page.

# runs with:
# sudo nohup python3 kickbot_manager.py </dev/null >football_manager.log 2>&1 &
# (must sudo to give it permission to write over the user_input file)


# import statements
import json
import multiprocessing
from TWITBOT import Twitbot
from KICKBOT import Kickbot
import READER as Reader

import time
import RPi.GPIO as GPIO

# button input
KICK_BUTTON = 20
GPIO.setup(KICK_BUTTON, GPIO.IN)

# setup
# note that pins are setup in KICKBOT.py

twitbot = Twitbot()
kickbot = Kickbot()


# clears out input from previous runs
Reader.wipe()

# stores most recent mention in cache
twitbot.updateLastMention()

# initializes a multiprocessing array used to communicate between
# the twit_check subprocess and the main loop
TWITTER_OVERRIDE = multiprocessing.Array("f", 3)
TWITTER_OVERRIDE[0] = 0 # used as a true/false flag to override html check
TWITTER_OVERRIDE[1] = 0 # stores location extracted from tweets
TWITTER_OVERRIDE[2] = -1 # stores goal status. 0 and 1 for goal/miss, -1 for no shot.

SOURCE='' # tracks source of kick commands
    


# runs in a continuous loop via multiprocessing. Checks the kickbot twitter account
# for new mentions; when present, extracts the instructions and posts a confirmation
# on the twitter account.
# must be run as a seperate process, because twitter's data limits for developer
# accounts limits bots to checking twitter accounts no more than 15 times in 15
# minutes; seperate processes allow this process to check twitter once every few
# minutes while allowing the main process to check for html input every few
# seconds.
def twit_check():
    
    # stores user info between loops
    TWITTER_NAME = ""
    TWITTER_HANDLE = ""
    
    while 1:
        
        # checks to see if main process has returned a goal or no goal result
        # for a shot taken from twitter. If so, creates a post containing
        # the user name and twitter handle of the person to take the shot, and
        # whether or not that shot resulted in a goal, then posts it to the
        # bot's twitter account.
        if (TWITTER_OVERRIDE[2] == 1 or  TWITTER_OVERRIDE[2] == 0):
            goal = TWITTER_OVERRIDE[2]
                                
            if (goal):
                goal_post = "and scored!"
            else:
                goal_post = "but did not score :("      
             
            post_string = "Twitter user {} (@{}) has kicked from {:.2f}, {}".format(TWITTER_NAME, TWITTER_HANDLE, TWITTER_OVERRIDE[1], goal_post)
                
            # posts to twitter
            twitbot.post(post_string)
        
        # resets the goal status
            TWITTER_OVERRIDE[2] = -1       
        
        
        
        # checks bot's twitter feed to see if any user has tweeted a shot
        # command to the bot. If so, stores their user name and twitter handle,
        # and passes the command to the main code.
        if (twitbot.updateLastMention()):
                     
            user_name = twitbot.lastMention[1]
            tweet_handle = twitbot.lastMention[2]
            location = float(twitbot.lastMention[3])
            
            # passes location to main process. TWITTER_OVERRIDE[0] tells
            # the main process to run the command from twitter and ignore
            # input from the html page until the twitter shot has completed.
            TWITTER_OVERRIDE[0] = 1
            TWITTER_OVERRIDE[1] = location
            
            # used to format a twitter post after the shot has completed.
            TWITTER_NAME = user_name
            TWITTER_HANDLE = tweet_handle
            
            
        
        # waits >1 minute between reads to stay comfortably within twitter
        # data rate limits
            # may be set to 30 seconds during a demonstration so the presentation
            # doesn't have to spend 2 minutes waiting. This is okay but only for
            # a short demonstration; set back to >60 for regular operation.
        time.sleep(150)
        

# starts twitter check as a daemon process
twitter_cycle = multiprocessing.Process(target=twit_check, args=())
twitter_cycle.daemon = True
twitter_cycle.start()

# initializes location at 0
location = 0.0     
# initializes a non-boolean value to goal status to represent
# neither a goal nor a missed shot
goal = -1

while 1:
       
    # First checks to see if instructions have been passed from
    # twit_check process.
    # (twitter commands have priority because of the lag between
    # twitter checks)
    if(TWITTER_OVERRIDE[0]):
        waiting = False
        location = location + float(TWITTER_OVERRIDE[1])
        SOURCE = "twitter"
        
    # kick button override
    elif (GPIO.input(KICK_BUTTON)):
        waiting = False
        print("KICKBUTTON")
        # ie, kick from current location
        location = location
        SOURCE = "kick button"
            
    
    # reads html instructions from user_input.txt, but only
    # when the twitter_override flag == 0 and the kick_button hasn't
    # been pressed
    else:
        # the first file read or two after the html updates results in an error;
        # dummyRead() clears this out by sending a pair of  dummy read commands
        # to the file.
        # if both commands result in an error, dummyRead() returns True, and
        # this code pauses for 2 seconds before attempting to read the file.
        if(Reader.dummyRead()): time.sleep(2)
        
        waiting = Reader.waiting()
        time.sleep(.2)
        loc = Reader.location()
        #print("html command from {}".format(loc))
        if (loc != "end"):
            location = location + float(loc)*.5
        else:
            location = "end"
        SOURCE = "this page"
        

            
        
    # if waiting == true, no new command has been issued, and continues
    # without kicking.
    # if location == "end", terminates the program
    if (waiting): continue
    elif (location == "end"): break

    
    
    # sends a kick command to user-defined location. print() commands are not
    # displayed to user; instead they print to football_manager.log 
    location = float(location)
    print("kick command at location {} recieved from {}. passing command".format(location, SOURCE))
    goal = kickbot.kick(location)
    print("Kick completed. goal status = {}".format(goal))

    
    # resets twitter_override array if instructions were
    # passed from twitter feed
    if(TWITTER_OVERRIDE[0]):
                      
        # resets override flags and sends goal status to twit_check daemon
        TWITTER_OVERRIDE[0] = 0
        TWITTER_OVERRIDE[1] = 0
        TWITTER_OVERRIDE[2] = goal

    
    # clears out command file and reports goal status
    Reader.report(goal, SOURCE)
        
    time.sleep(5)




# cleanup; this code executes when processes
# terminated by the user inputting "end" into the html.

GPIO.cleanup()
twitter_cycle.terminate()
print("successful shutdown, good game")


















