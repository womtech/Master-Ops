#!/usr/bin/python
import os, time, datetime

# Author: MD Danish <danish@whackedout.in>
# Utility: Error Logger
# Date Written: Dec 31, 2018
# Usage: ErrorLogger(message='Error Text Goes Here')

'''
Function to Log the error
Message <string>
'''
def ErrorLogger( Message ):
    logwd = '/projects/mops/Logs/'
    currentTime = str(time.localtime(time.time()).tm_hour)+' '+ str(time.localtime(time.time()).tm_min)+' '+str(time.localtime(time.time()).tm_sec)
    currentDate = datetime.date.today().strftime("%d_%B_%Y")
    logFileName = logwd + currentDate + '.txt'
    if os.path.exists( logFileName ):
        append_write = 'a'
    else:
        append_write = 'w'
    handler = open( logFileName, append_write )
    handler.write( currentTime + ':=> ' + Message + '\n')
    handler.close(  )
    return

