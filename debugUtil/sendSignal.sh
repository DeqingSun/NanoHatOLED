#!/bin/bash

if [ $# -ne 1 ]
then
    echo "you must give exactly 1 parameters for button. use 1, 2 or 3"
else
    if [ $1 -eq 1 ]; then
        echo "send k1"
        sudo kill -SIGUSR1 $(ps aux | grep bakebit_nanohat_oled.py | grep -v grep | grep -v sudo | awk '{print $2}')
    elif [ $1 -eq 2 ]; then
        echo "send k2"
        sudo kill -SIGUSR2 $(ps aux | grep bakebit_nanohat_oled.py | grep -v grep | grep -v sudo | awk '{print $2}')        
     elif [ $1 -eq 3 ]; then
        echo "send k3"
        sudo kill -SIGALRM $(ps aux | grep bakebit_nanohat_oled.py | grep -v grep | grep -v sudo | awk '{print $2}')  
    fi;
fi;



