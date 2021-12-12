#!/usr/bin/python37all

# file should be saved in ~/cgi (no subfolders)
# remember to sudo chmod 755 this file 

# assumes project files are in ~/ENME441/441_final

import cgi
import cgitb
cgitb.enable()
import json

try:
    with open("/home/pi/ENME441/441_final/user_input.txt", 'r') as f:
      data = json.load(f)
      
      goal = data["goal"]
      source = data["source"]
except:
    goal = -1
    source = -1


data = cgi.FieldStorage()

settings = {"waiting":data.getvalue("waiting"), 
            "position":data.getvalue("position"),
            "goal":goal,
            "source":source}

with open("/home/pi/ENME441/441_final/user_input.txt", 'w') as f:
  json.dump(settings, f)
  




# rebuilds web page
print("""Content-type: text/html\n\n
<html>

<head>
    <title>Kickbot @ UMD!</title>
    <style>
        header {
            background-color:darkgray;
            padding:30px;
            text-align:center;
            font-size:42px;
            color:white;
        }
        nav {
            float:left;
            width:30%;
            height:600px;
            background-color:gainsboro;
            text-align:center;
            font-size:18px;
        }
        article {
            float:left;
            width:70%;
            height:600px;
            background-color:floralwhite;
            text-align:center;
            font-size:24px;
        }
    </style>
</head>

<body style="background-color:lightgreen"
<br>

<header>
    <h2>O Jogo Botnito</h2>
</header>

<nav>
<br>
<br>
<form action = "/cgi-bin/kickbot.cgi" method = "POST">

        <input type = "hidden" name="waiting" value="0">

        <label for="position">Enter a distance (in inches)<br> to move the kicker:</label><br>
        <input type = "text" id="position" name="position"><br>


    <input type = "submit" value="Move & Kick!">
</nav>


<article>
<br>
<br>
Welcome to Kickbot at University of Maryland! 
    <pre>Use the command window to the left to move the kicker. 
    Negative values move the kicker to the right; positive values 
    move it left.
    </pre>

""")

# prints results and source of last shot taken
if (goal == True):
    print("<br>Last shot taken from {}, and scored!".format(source))

elif (goal == False):
    print("<br>Last shot taken from {}, and missed".format(source))



print("""
</article>
</body>
</html>
""")

