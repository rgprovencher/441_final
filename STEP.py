import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
from math import pi


# radius of pully driven by step motor, used to convert theta to distance
RADIUS = 1


# 8 half-steps per cycle, 8 cycles per revolution, into a 1:64 gearbox = half-steps per full revolusion 
# # 360 degrees per rev  /  no. of half-steps pre rev = degrees per half-step
# = 0.0879 deg; 
STEP_ANGLE = 0.0879

# distance moved in one half-step, same units as radius
# note conversion of STEP_ANGLE from degrees to radians
STEP_DISTANCE = float(RADIUS * ( STEP_ANGLE* pi/180 ))

# delay between halfsteps, in usec
STEP_DELAY = 2000


class Stepper:

    def __init__(self, p0, p1, p2, p3):
        self.pins = [p0, p1, p2, p3]
        
        for pin in self.pins:
          GPIO.setup(pin, GPIO.OUT, initial=0)
        

        # Define the pin sequence for counter-clockwise motion, noting that
        # two adjacent phases must be actuated together before stepping to
        # a new phase so that the rotor is pulled in the right direction:
        self.sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
                [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
        
        self.state = 0 # tracks location within the stator sequence
        

        # initializes starting angle
        self.theta = 0.0
        
        # initializes starting position
        self.position = 0.0
        
       

    def __delay_us(self, tus): # use microseconds to improve time resolution
      endTime = time.time() + float(tus)/ float(1E6)
      while time.time() < endTime:
        pass
    
    
    def __halfstep(self, dir):
        # dir = +/- 1 for ccw, cw
        
        self.state += dir;
        if self.state > 7:
            self.state = 0
            #print()
        elif self.state < 0:
            self.state = 7
            #print()
        
        for pin in range(4):
            GPIO.output(self.pins[pin], self.sequence[self.state][pin])
        
        #print("{} ".format(self.state), end='')
            
        self.__delay_us(STEP_DELAY)

        

        self.theta += dir*STEP_ANGLE
        self.position += dir*STEP_DISTANCE
        
        # only used when stepper position needs to be bound within 360
        #self.theta = self.theta % 360.0
        
        
    def __moveSteps(self, steps, dir):
        # move actuation sequence a given number of half-steps
        
        for step in range(steps):
            self.__halfstep(dir)
    
    
    # reports current angle when called.
    def angle(self):
        return self.theta
              

        
    # given an angle, determines the nearest direction for the arm to
    # turn. Returns +1 for ccw, -1 for cw.
    def __nearest(self, angle):
      
      if (self.theta - angle)%360 < 180: dir = -1
      else: dir = 1

      return dir
    
    

    # gien an angle, rotates the cardboard arm to that angle.
    def goAngle(self, angle):
      # %360 converts <0 and >360 inputs to a 0-360 range
      angle = float((angle) % 360 )

      # find nearest turning direction 
      dir = self.__nearest(angle) 
      
      while abs(self.theta-angle) > 0.15:
        self.__halfstep(dir)
        # print("angle:  {} theta: {} diff: {}".format(angle, self.theta, abs(self.theta-angle)))
        
        
    def goTo(self, location):
        # returns 1 if location is greater than current position, -1 if less
        dir = int((location-self.position)/abs(location-self.position))
        j = 0
        
        while (abs(location-self.position) > 0.1):
            self.__halfstep(dir)
    
    def test(self):
        for i in range (20):
            self.__halfstep(1)
            time.sleep(.2)
        

    
