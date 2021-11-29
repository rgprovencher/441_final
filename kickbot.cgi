#!/usr/bin/python37all

# DO NOT FORGET to sudo chmod 755 this file (rob you set an alias 
# 'allow4' ='sudo chmod 755 ~cgi/441/*.py')
# assumes project files are in ~/ENME441/441_final

import cgi
import cgitb
cgitb.enable()
import json

data = cgi.FieldStorage()

settings = {"position":data.getvalue("position"), "speed":data.getvalue("speed")
}

with open("/home/pi/ENME441/441_final/user_input.txt", 'w') as f:
  json.dump(settings, f)



# to do: open post.txt to display tweets, or vids



print("""Content-type: text/html\n\n

<html>
  <form action - "/cgi-bin/441/kickbot.cgi" method = "POST">
    <input type = "hidden" id="waiting" name="waiting" value="False">
    <label for="position">Location:</label><br>
    <input type = "text" id="position" name="position"><br>
    <input for="speed">Power:</form><br>
    <input type = "text" id="speed" name="speed"><br>
    <input type = "submit" value="Kick">
</html>



""")

