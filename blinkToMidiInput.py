import os
import errno
import RPi.GPIO as GPIO
import time

#this scripts reads a PIPE and blinks the blue LED every time a line is read

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting pin 25 as an output pin
GPIO.setup(25,GPIO.OUT)

FIFO = '/home/pi/readmidi'


try:
    os.mkfifo(FIFO)
except OSError as oe: 
    if oe.errno != errno.EEXIST:
        raise

print("Opening FIFO...")
fd = open(FIFO,"r")

#start loop
while True:
    #set PIPE-line to variable 
    line = fd.readline()
    
    #if the line is not empty
    if line != "":
        print(line)

        #turn on blue LED
        GPIO.output(25,GPIO.HIGH)
        
        #wait 0.05 sec
        time.sleep(0.05)
        
        #turn off blue LED
        GPIO.output(25,GPIO.LOW)

