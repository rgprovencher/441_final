#!/usr/bin/python37all

# file should be saved in ~/cgi (no subfolders)
# DO NOT FORGET to sudo chmod 755 this file 
# 			(rob you set an alias 'allowa' ='sudo chmod 755 ~cgi/441/*')
# assumes project files are in ~/ENME441/441_final

import cgi
import cgitb
cgitb.enable()
import json

data = cgi.FieldStorage()

settings = {"waiting": data.getvalue("waiting"), 
            "position":data.getvalue("position")}

with open("/home/pi/ENME441/441_final/user_input.txt", 'w') as f:
  json.dump(settings, f)




# rebuilds webpage

print("""Content-type: text/html\n\n
<html>
<br>

<form action = "/cgi-bin/kickbot.cgi" method = "POST">

        <input type = "hidden" name="waiting" value="False">

        <label for="position">Location:</label><br>
        <input type = "text" id="position" name="position"><br>


    <input type = "submit" value="Kick">
    
</html>


""")

