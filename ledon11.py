import RPi.GPIO as GPIO
import time

#this scripts turns on the green LED at pin 11 by setting it to HIGH, outputing 3.3 V 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)

print ("LED on")

GPIO.output(11,GPIO.HIGH)
time.sleep(1)
