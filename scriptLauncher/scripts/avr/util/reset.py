#!/usr/bin/python

import sys
import serial

try:
    com = serial.Serial(sys.argv[1], 1200)
    com.dtr=False
    com.close()
except:
    exit(1)

exit(0)


