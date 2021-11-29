import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


# SG92R microservo
# 20 msec pulse     ---->     50 Hz duty cycle
# 0 deg at 1 msec pulse          0 at 0%
# 90 at 1.5 msec                 90 at 5%
# 180 at 2 msec                  180 at 10%

DUTY_CYCLE = 50
ZERO = 1
FULL = 12.6


class Servo:
    
    def __init__(self, cmd):
        
        self.cmd = cmd
        GPIO.setup(self.cmd, GPIO.OUT)
        self.pwm = GPIO.PWM(self.cmd, DUTY_CYCLE) # 50 Hz pwm on servo pin
        
        self.pwm.start(0)
        #self.__goAngle(0)
    
    def __goAngle(self, angle):
        
        # clean up input data
        angle = angle % 180
        # convert angle from degrees to a pwm %
        angle = float((angle/180))*float((FULL-ZERO)) + ZERO
        
        
        self.pwm.ChangeDutyCycle(angle)

    
    def kick(self):
        
        # kick out fast
        for i in range (0, 181, 1):
            self.__goAngle(i)
            time.sleep(0.001)
        
        # pause
        time.sleep(1)

        
        # retract slow
        for j in range(180, -1, -1):
            self.__goAngle(j)
            time.sleep(0.001)
        
    
    
        
        
