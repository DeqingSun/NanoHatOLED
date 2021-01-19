#!/bin/bash

#install avrdude
#sudo apt-get update
#sudo apt-get install avrdude

#set rules in /etc/udev/rules.d

echo "Run avrdude..."
avrdudeOutput=$(avrdude -v -patmega32u4 -cstk500v2 -Pusb 2>&1)
avrdudeReturn=$?
if [ $avrdudeReturn -eq 0 ]
then
    echo "ATmega32u4 found!"
else
    if [[ $avrdudeOutput == *"did not find any USB device"* ]]; then
        echo "AVRISP MKII unplugged."
    elif [[ $avrdudeOutput == *"bad AVRISPmkII connection status"* ]]; then
        echo "Bad connection"
    elif [[ $avrdudeOutput == *"Double check chip"* ]]; then
        echo "Double check chip"
    else
        echo "check /run for err"   
    fi
    echo $avrdudeOutput > /run/avrdudeOutput.txt
    exit 1
fi

echo "Erase and set fuses."
#lock bit 6bit
avrdudeOutput=$(avrdude -v -patmega32u4 -cstk500v2 -Pusb -e -Ulock:w:0xFF:m -Uefuse:w:0xcb:m -Uhfuse:w:0xd8:m -Ulfuse:w:0xff:m 2>&1)
avrdudeReturn=$?
if [ $avrdudeReturn -eq 0 ]
then
    echo "ERASE OK."
else
    echo ".check /run for err"   
    echo $avrdudeOutput > /run/avrdudeOutput.txt
    exit 1
fi
 
echo "6s to prog&lock."
avrdudeOutput=$(avrdude -v -patmega32u4 -cstk500v2 -Pusb -Uflash:w:/home/pi/avrfiles/Caterina-Leonardo_short.hex:i -Ulock:w:0xEF:m 2>&1)
avrdudeReturn=$?
if [ $avrdudeReturn -eq 0 ]
then
    echo "BOOTLOADER OK."
else
    echo "..check /run for err"   
    echo $avrdudeOutput > /run/avrdudeOutput.txt
    exit 1
fi


