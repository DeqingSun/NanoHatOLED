#!/bin/bash

#This is for turebird round touchscreen Arduino board. Updated for firmware 20190415

#set rules in /etc/udev/rules.d

echo "RESET Leonardo..."
/home/pi/avrfiles/leonardoUploader /dev/ttyACM0
sttyReturn=$?
if [ $sttyReturn -eq 0 ]
then
    echo "Reset OK"
else
    echo "Reset ERR"   
    exit 1
fi

sleep 2

avrdudeOutput=$(avrdude -patmega32u4 -cavr109 -v -P/dev/ttyACM0 -b57600 -D -Uflash:w:/home/pi/avrfiles/sketch_touchScreenHID.ino.hex:i 2>&1)
avrdudeReturn=$?

if [ $avrdudeReturn -eq 0 ]
then
    echo "FW OK!"
else
    echo "check /run for err"   
    echo $avrdudeOutput > /run/avrdudeOutput.txt
    exit 1
fi

sleep 2

lsusbOutput=$(lsusb)
if [[ $lsusbOutput == *"Arduino SA Leonardo (CDC ACM, HID)"* ]]; then
    echo "HID OK"
else
    echo "HID not found"
fi

exit 0

