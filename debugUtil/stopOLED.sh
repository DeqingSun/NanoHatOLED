#!/bin/bash

sudo kill $(ps aux | grep 'bakebit_nanohat_oled' | awk '{print $2}')
sudo pkill NanoHatOLED
#sudo /usr/local/bin/oled-start
