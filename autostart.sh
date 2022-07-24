#/usr/bin/bash

#this script runs in the background, checking if ttymidi and fluidsynth is running and checking if they are connected
#it also does a bit off turning on and off the green LED

#start endless loop
while true; do

    #is ttymidi running ?
    if pgrep -x "ttymidi-sysex" > /dev/null
    	
    then
	echo "ttymidi is running"
    else
        echo "starting ttymidi"

	#turn off the green LED
    	/usr/bin/python3 /home/pi/ledoff11.py

	#starts ttymidi and send output to a PIPE, readmidi
	/home/pi/ttymidi-sysex -s /dev/ttyAMA0 -v -b 38400 > /home/pi/readmidi &

    fi

    #figure out what number the USB soundard has according to the alsamixer, by calling "aplay"
    usbSndCard=$(aplay -l | grep "USB PnP Sound" | awk -F" " '{ print $2 -0 }')

    #if the soundcard isn't initialized
    if [ -z "$usbSndCard" ] 
    then

	echo "Soundcard not ready"
    
    else

	#is fluidsynth running ?
    	if pgrep -x "fluidsynth" > /dev/null 
    	then 
		echo "Fluidsynth is running"
    	else

		echo "Starting Fluidsynth..."

		#turning off green LED
    		/usr/bin/python3 /home/pi/ledoff11.py

		#starting fluidsynth
		/usr/bin/tmux new -d -s fluidsynth "fluidsynth -C0 -R0 -a alsa -o audio.alsa.device=hw:$usbSndCard /home/pi/viktorbass.sf2"
	
		#sleep 5 sec
		sleep 5
    	fi
    fi

    #check if fluidsynth och ttymidi are connected, ny checking if the word "Connected" is in the output of "aconnect -l"
    aconn=$(aconnect -l | grep "Connected")
    
    #if "Connected is not present"
    if [ "$aconn" = "" ];
    then
	
	echo "Fluidsynth and ttymidi are NOT connected" 
	
    	#turn off green LED
	/usr/bin/python3 /home/pi/ledoff11.py

	#get device numbers for fluidsynth and ttymidi, with "aconnect -l" 
        ttymidi=$(aconnect -l | grep "ttymidi" | awk -F" " '{ print $2 -0 }') 
        fluidsynth=$(aconnect -l | grep "FLUID" | awk -F" " '{ print $2 -0 }') 
	
	echo "Connecting rrymidi and Fluidsynth...."

	#connecting ttymidi and fluidsynth with some help of the numbers accuired earlier
	aconnect "$ttymidi":0 "$fluidsynth":0

    else
	echo "Fluidsynth and ttymidi are connected" 
    fi

    #turning ON the green LED
    /usr/bin/python3 /home/pi/ledon11.py
    
    echo "Everything is as it should, resting 10 seconds"
    sleep 10


done
