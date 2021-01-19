#!/bin/bash

#install openocd
#sudo apt-get update
#sudo apt-get install openocd

#set rules in /etc/udev/rules.d

#erase
#  openocd -d2 -s /usr/share/openocd/scripts -f /home/pi/openocdfiles/arduino_zero.cfg -c "telnet_port disabled; init; halt; at91samd chip-erase; reset; shutdown "

echo "ERASE over openocd..."
openocdOutput=$(openocd -d2 -s /usr/share/openocd/scripts -f /home/pi/openocdfiles/arduino_zero.cfg -c "telnet_port disabled; init; halt; at91samd chip-erase; reset; shutdown " 2>&1)
openocdReturn=$?
if [ $openocdReturn -eq 0 ]
then
    echo "ERASE OK"
else
    if [[ $openocdOutput == *"unable to find CMSIS-DAP device"* ]]; then
        echo "CMSIS-DAP unplugged."
    else
        echo "check /run/user/1000 for err"   
    fi
    echo $openocdOutput > /run/user/1000/openocdOutput.txt
    exit 1
fi

