import RPi.GPIO as GPIO
import time

#this 
#this scripts turns off the green LED at pin 11 by setting it to LOW, outputing 0 V

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
time.sleep(1)
print ("LED off")
GPIO.output(11,GPIO.LOW)
