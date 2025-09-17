import time, sys, math
from grove.adc import ADC

__all__ = ["GroveLightSensor"]

#-----------------------#
#   Hyper Parameter     #
#-----------------------#

st = 1          # sleep time
lt = 30         # light threshold
lspin = 6       # light sensor pin

#-----------------------#
#   Main code           #
#-----------------------#

class GroveLightSensor(object):
    '''
    Grove Light Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        '''
        Get the light strength value, maximum value is 100.0%

        Returns:
            (int): ratio, 0(0.0%) - 1000(100.0%)
        '''
        value = self.adc.read(self.channel)
        return value
    
Grove = GroveLightSensor

def detect_one_byte(sensor):
    byte_msg = ""
    for _ in range(0,8) :
        if sensor.light >= lt:
            byte_msg += '1'
        else :
            byte_msg += '0'
        time.sleep(st)
    return byte_decode(byte_msg)
        
def byte_decode(byte_msg):
    # add bin format to string ex : 0b01000001 
    byte_msg = '0b' + byte_msg 
    c = int(byte_msg,2) # change string for binary to decimal integer
    return chr(c)

def main(pin=lspin):
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    num =''
    msg = ''
    sensor = GroveLightSensor(pin)
    
    print("Waiting for start signal...")

    while sensor.light < lt:
        continue
    
    print('Find the start signal, start.')
    time.sleep(st)
    
    num = ord(detect_one_byte(sensor)) # 8-bit message length
    print(num)
    print("Receiving message...")
    for _ in range(0,int(num)):
        msg += (detect_one_byte(sensor)) # Read length n-byte message
    
    print(f'Message length: {num}, Message decode: {msg}') # print result
    
if __name__ == '__main__':
    main()
