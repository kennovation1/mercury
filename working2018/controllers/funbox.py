# Example controller that reads switches and controller light outputs based on somewhat arbitrary mapping rules
# python readinputs.py -f &
# python lightoutupts.py &
# python funbox.py

import json
import os
import errno
from time import sleep

SwitchesFIFO = '/tmp/mercury-events'
LightsFIFO = '/tmp/light-commands'

Intensity = 50
DIM = 50
BRIGHT = 150
WarnIntenity = DIM

def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise

def handleSwitchEvent(event):
    eventName = event['eventName']

    if eventName == 'LIGHT TEST=>ON':
        lightTest(on=True)
    elif eventName == 'LIGHT TEST=>OFF':
        lightTest(on=False)
    elif eventName == 'WARN LIGHTS=>DIM':
        setWarnLightsBrightness(bright=False)
    elif eventName == 'WARN LIGHTS=>BRIGHT':
        setWarnLightsBrightness(bright=True)

def lightTest(on):
    message = { 'type': 'LOGICAL', 'target': 'all', 'action': 'off', 'intensity': Intensity }
    if on:
        message['action'] = 'on'
    sendLightCommand(message)

def setWarnLightsBrightness(bright):
    WarnIntensity = DIM
    if bright:
        WarnIntensity = BRIGHT

    # TODO: Create a loop over the 10 warn lights that are on and set intensity. Any new warn lights that are enabled
    # should use WarnIntensity and not Intensity
    target = 'CABIN PRESS'
    message = { 'type': 'LOGICAL', 'target': target, 'action': 'on', 'intensity': WarnIntensity }
    sendLightCommand(message)

def sendLightCommand(message):
    # Newline makes it possible to use readline on the other size so that I have a good message boundary
    buff = json.dumps(message) + '\n'
    LightsFp.write(buff)
    LightsFp.flush()


############
# Main
############

makeFifo(SwitchesFIFO)
makeFifo(LightsFIFO)

# Open and writes will block if no reader on fifo (or if full)
LightsFp = open(LightsFIFO, 'w')

# Open will block until there is a writer and a message is written
with open(SwitchesFIFO, 'r') as switchesFp:
    while True:
        # This does not block. Will return 0 if nothing to read
        mesg = switchesFp.readline()
        if len(mesg) > 0:
            event = json.loads(mesg)
            print(json.dumps(event, indent=4))
            handleSwitchEvent(event)
        else:
            # Could go off and do other things here...
            pass

LightsFp.close()
