#!/usr/bin/env python
#
# This is a script launcher for NanoHat OLED
#
# The script list all scripts in /home/pi/scripts/
#
# Use K1 to scroll up, K2 to scroll down, K3 to select
#
# Deqing Sun 2018

'''
## License

The MIT License (MIT)

BakeBit: an open source platform for connecting BakeBit Sensors to the NanoPi NEO.
Copyright (C) 2016 FriendlyARM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


import bakebit_128_64_oled as oled
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import sys
import subprocess
import threading
import signal
import os
import socket
import threading
import Queue

ON_POSIX = 'posix' in sys.builtin_module_names

global width
width=128
global height
height=64

global scriptPath
scriptPath = '/home/pi/scripts/'

global scriptIndex
scriptIndex=0
global displayBeginIndex
displayBeginIndex=0

oled.init()  #initialze SEEED OLED display
oled.setNormalDisplay()      #Set display to normal mode (i.e non-inverse mode)
oled.setHorizontalMode()

global drawing 
drawing = False

global image
image = Image.new('1', (width, height))
global draw
draw = ImageDraw.Draw(image)
global smartFont
smartFont = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 10);

global lock
lock = threading.Lock()

global triggerExecution
triggerExecution = False

global scriptOutput
scriptOutput = ''

global runningSubprocess
runningSubprocess = None

global subprocessQueue
global subprocessReadThread

subprocessQueue = Queue.Queue()
subprocessReadThread = None

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    #print 'enqueue_output END'

def draw_page():
    global drawing
    global image
    global draw
    global oled
    global smartFont
    global width
    global height
    global scriptPath
    global scriptIndex
    global displayBeginIndex
    global width
    global height
    global lock
    global triggerExecution
    global scriptOutput
    global runningSubprocess
    global subprocessQueue
    global subprocessReadThread

    lock.acquire()
    is_drawing = drawing
    lock.release()

    if is_drawing:
        return

    lock.acquire()
    drawing = True
    scriptIndexDrawing = scriptIndex;
    lock.release()
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)       #clear img
    if (not os.path.isdir(scriptPath)) : 
        draw.text((0, 0),'Script Path not Found!', font=smartFont, fill=255)
        draw.text((0, 12),scriptPath, font=smartFont, fill=255)
    else:
        scriptsInPath = os.listdir(scriptPath)
        filesCount = len(scriptsInPath)
        scriptsInPath.sort()    #list and sort file
        scriptIndexDrawingPrev = scriptIndexDrawing
        if (filesCount == 0 ):
            scriptIndexDrawing = 0
        elif (scriptIndexDrawing<0):
            scriptIndexDrawing+=filesCount
        elif (scriptIndexDrawing>=filesCount):
            scriptIndexDrawing-=filesCount
        if (scriptIndexDrawing != scriptIndexDrawingPrev):      #write value back if there is any change
            lock.acquire()
            scriptIndex = scriptIndexDrawing
            lock.release()
            
        displayIndex = scriptIndexDrawing+1;
        if (filesCount == 0):
            displayIndex = 0
            displayBeginIndex = 0
        
        #for file in scriptsInPath:
        #    print file
        draw.text((0, 0),'Script: '+str(displayIndex)+' of '+ str(filesCount), font=smartFont, fill=255)
        draw.line((0,12,127,12), fill=255)
        
        if (filesCount > 0):    #checkdisplayEntry
            if (scriptIndexDrawing<displayBeginIndex):
                displayBeginIndex = scriptIndexDrawing;
            if (scriptIndexDrawing>displayBeginIndex+2):
                displayBeginIndex = scriptIndexDrawing-2;
        itemDisplaying = 3;
        if (filesCount < 3):
            itemDisplaying = filesCount
            displayBeginIndex = 0
        try:        
            for i in range(itemDisplaying): #displayEntry from displayBeginIndex
                fillColor = 255
                index = displayBeginIndex+i
                if (scriptIndexDrawing == index):
                    fillColor = 0
                    draw.rectangle((0,13+12*i-1,width,13+12*i+12), outline=0, fill=255)
                    if (runningSubprocess is not None):
                        if (runningSubprocess.poll() == None):
                            draw.rectangle((width-10,13+12*i-1+2,width-2,13+12*i+12-2), outline=0, fill=0)
                draw.text((1, 13+12*i),scriptsInPath[index], font=smartFont, fill=fillColor)
        except:
            pass    #something edit script alive may cause array out of bound error
            
        draw.line((0,49,127,49), fill=255)

        draw.text((1, 13+12*3+1), scriptOutput, font=smartFont, fill=255)
        
        #check script execution
        needToExecute = False;
        lock.acquire()
        needToExecute = triggerExecution;
        if (triggerExecution):
            triggerExecution = False;
        lock.release()
        if ((filesCount > 0) and (needToExecute == True)):
            fileToExecute = scriptPath + scriptsInPath[scriptIndexDrawing]
            if (runningSubprocess is not None):
                if (runningSubprocess.poll() == None):
                    print 'Kill previous running script'
                    runningSubprocess.kill()
            print 'Execute : '+ fileToExecute
            try:
                runningSubprocess = subprocess.Popen(fileToExecute, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=ON_POSIX)
                subprocessReadThread = threading.Thread(target=enqueue_output, args=(runningSubprocess.stdout, subprocessQueue))
                subprocessReadThread.daemon = True # thread dies with the program
                subprocessReadThread.start()
            except Exception as e:
                print('Popen error occured.')
                print(e)
        #check running script
        if (runningSubprocess is not None):
            while True:
                try:  line = subprocessQueue.get_nowait() # or q.get(timeout=.1)
                except Queue.Empty:
                    #print('no output yet')
                    break;
                else: # got line
                    line = line.strip()
                    scriptOutput = line
                    #print scriptOutput

    oled.drawImage(image)

    lock.acquire()
    drawing = False
    lock.release()

def update_page_index(delta):
    global scriptIndex
    lock.acquire()
    scriptIndex += delta
    lock.release()

def receive_signal(signum, stack):
    global triggerExecution

    if signum == signal.SIGUSR1:
        print 'K1 pressed'
        update_page_index(-1)
        draw_page()

    if signum == signal.SIGUSR2:
        print 'K2 pressed'
        update_page_index(1)
        draw_page()


    if signum == signal.SIGALRM:
        print 'K3 pressed'
        lock.acquire()
        triggerExecution = True
        lock.release()
        draw_page()

##main code

image0 = Image.open('scriptrunner.png').convert('1')
oled.drawImage(image0)
time.sleep(1)

signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)
signal.signal(signal.SIGALRM, receive_signal)

while True:
    try:
        draw_page()

        time.sleep(0.3)
    except KeyboardInterrupt:                                                                                                          
        break                     
    except IOError:                                                                              
        print ("Error")
