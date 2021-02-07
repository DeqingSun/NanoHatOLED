#!/bin/bash

#This is for funkey Arduino board. Updated for firmware 

#set rules in /etc/udev/rules.d

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "RESET Funkey..."
python "$SCRIPT_DIR"/util/reset.py "/dev/ttyACM0"
sttyReturn=$?
if [ $sttyReturn -eq 0 ]
then
    echo "Reset OK"
else
    echo "Reset ERR"   
    exit 1
fi

sleep 2

echo "Uploading"
avrdudeOutput=$(avrdude -patmega32u4 -cavr109 -v -P/dev/ttyACM0 -b57600 -D -Uflash:w:"$SCRIPT_DIR"/util/funkey.hex:i 2>&1)
avrdudeReturn=$?

#!!!!

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
if [[ $lsusbOutput == *"20a0:4267"* ]]; then
    echo "FUNKEY OK"
else
    echo "FUNKEY not found"
fi

exit 0

