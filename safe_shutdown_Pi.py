import time
import RPi.GPIO as GPIO

#this script run in the background and listens for a button press and then safely turns off the Pi
#much of the code is nicked from this page:
#https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button/

#defines what pin is doing what
shutdown_pin = 24
power_pin = 22


# Suppress warnings
GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

#pin number 22 will only be high, output 3,3 V
GPIO.setup(power_pin, GPIO.OUT)
GPIO.output(power_pin, 1)


# Use Qwiic pHAT's pullup resistor so that the pin is not floating
GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# modular function to shutdown Pi
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


# Check button if we want to shutdown the Pi safely
while True:
    
    #short delay, otherwise this code will take up a lot of the Pi's processing power
    time.sleep(0.5)

    # For troubleshooting, uncomment this line to output buton status on command line
    #print('GPIO state is = ', GPIO.input(shutdown_pin))
    if GPIO.input(shutdown_pin)== 1:
        shut_down()
