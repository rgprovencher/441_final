# class object intended to simplify interacting with user_input.txt in the main code.

import json
import time

# the first read of the user_input.txt file after the cgi code writes into
# it always causes an error. dummyRead() clears that error out by sending a pair
# of dummy reads to the .txt file, which resolves the issue.
# If file is successfully
# read, returns False; if both read attepts return errors (hasn't
# happened yet, but just in case) returns True, which triggers main code to wait for
# a few seconds before attempting another read
def dummyRead():
    for i in range(2):
        try:
            with open("user_input.txt", 'r') as f:
                data = json.load(f)
                
            return False
        except:
            time.sleep(.2)
                    
    return True


# extracts and returns "waiting" variable from the user_input.txt file
def waiting():

    with open("user_input.txt", 'r') as f:
        data = json.load(f)
    
    return int(data["waiting"])

# extracts and returns "location" variable from the user_input.txt file
def location():

    with open("user_input.txt", 'r') as f:
        data = json.load(f)
    
    return data["position"]

# resets user_input.txt file to initial status
def wipe():
    INPUT_CLEAR = {"waiting":1, "position":0, "goal":-1, "source":-1}
    with open("user_input.txt", 'w') as f:
        json.dump(INPUT_CLEAR, f)

# used to write the result of a shot (goal or no goal) to the user input
# file, as well as the source of the command 
def report(goal, source):
    INPUT_CLEAR = {"waiting":1, "position":0, "goal":goal, "source":source}
    with open("user_input.txt", 'w') as f:
        json.dump(INPUT_CLEAR, f)
