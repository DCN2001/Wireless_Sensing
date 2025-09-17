import time
from scan_url import scanning
import RPi.GPIO as GPIO
# -----------------------#
#   Hyper Parameters     #
# -----------------------#

st = 1  # sleep time
led_pin = 27

# -----------------------#
#  Main code             #
# -----------------------#

def send_byte(byte):
    for bit in byte:
        if bit == '1':
            GPIO.output(led_pin, GPIO.HIGH)
        else:
            GPIO.output(led_pin, GPIO.LOW)
        time.sleep(st)
    GPIO.output(led_pin, GPIO.LOW) 

def main(message,message_length):

    # Start Signal
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(st)
    GPIO.output(led_pin, GPIO.LOW)

    # Send the message length
    length_byte = format(message_length, '08b')
    send_byte(length_byte)

    # Send each character of the message
    for char in message:
        byte_msg = format(ord(char), '08b')
        send_byte(byte_msg)

if __name__ == '__main__':
    try:
        # GPIO Configuration
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)
        
        MAC, url = scanning()
        message = url
        message_length = len(message)
        print(f"Transmit URL:{message}, Message length(by char):{message_length}")
        
        print("Transmit start.")
        main(message,message_length)
        print("Transmit done.")

    finally:
        GPIO.cleanup()
