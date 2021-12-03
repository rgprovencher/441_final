#!/usr/bin/env python3
#------------------------------------------------------
#
#       This is a program for PCF8591 Module.
#
#       Warnng! The Analog input MUST NOT be over 3.3V!
#    
#       In this script, we use a poteniometer for analog
#   input, and a LED on AO for analog output.
#
#       you can import this script to another by:
#   import PCF8591 as ADC
#   
#   ADC.Setup(Address)  # Check it by sudo i2cdetect -y -1
#   ADC.read(channal)   # Channal range from 0 to 3
#   ADC.write(Value)    # Value range from 0 to 255     
#
#------------------------------------------------------
import smbus
import time



class PCF8591:
    
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address



    def read(self, chn): #channel
        try:
            self.bus.write_byte(self.address,0x40 | chn)
           
            self.bus.read_byte(self.address) # dummy read to start conversion
        except Exception as e:
            print ("Address: %s \n%s" % self.address, e)
        
        return self.bus.read_byte(self.address)

    def write(self, val):
        try:

            self.bus.write_byte_data(self.address, 0x40, int(val))
        except Exception as e:
            print ("Error: Device address: 0x%2X \n%s" % self.address, e)
     
