#!/usr/bin/env python


import subprocess
import sys, os

pathname = os.path.dirname(sys.argv[0])
scriptFolder = os.path.abspath(pathname)

process = subprocess.Popen(scriptFolder+'/toolAndBin/vnproch55x '+scriptFolder+'/toolAndBin/tinyspiDw.bin', shell=True, stdout=subprocess.PIPE)
outputBuffer = ''

errorMessage = 'unknown ERR'
while True:
    output = process.stdout.read(1)
    #print >> sys.stderr, output
    if output == '' and process.poll() is not None:
        break
    if output:
        if (output!='\n' and output!='\r'):
            outputBuffer += output
        else:
            if (len(outputBuffer)>0):
                outputBuffer = outputBuffer.replace('\x1b[2K', '')
                if ('Found no CH55x USB' in outputBuffer):
                    errorMessage = 'CH55x not found'
                if ('Write' in outputBuffer):
                    print 'Write'
                if ('Verify' in outputBuffer):
                    print 'Verify'
            outputBuffer = ''
returnCode = process.poll()

if (returnCode==0):
    print 'wch551 flash OK'
else:
    print errorMessage

