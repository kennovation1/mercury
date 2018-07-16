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
WarnIntensity = DIM

WarnLightsState = {
        'CABIN PRESS': False,
        'O2 QUAN': False,
        'O2 EMER': False,
        'EXCESS SUIT H20': False,
        'EXCESS CABIN H20': False,
        'FUEL QUAN': False,
        'RETRO WARN': False,
        'RETRO RESET': False,
        'STBY AC-AUTO': False
        }

WarnAudioToneEvents = [
        'CABIN PRESS - AUDIO=>TONE',
        'O2 QUAN - AUDIO=>TONE',
        'O2 EMER - AUDIO=>TONE',
        'EXCESS SUIT H2O - AUDIO=>TONE',
        'EXCESS CABIN H2O - AUDIO=>TONE',
        'FUEL QUAN - AUDIO=>TONE',
        'RETRO WARN - AUDIO=>TONE',
        'RETRO RESET - AUDIO=>TONE'
        ]

WarnAudioOffEvents = [
        'CABIN PRESS - AUDIO=>OFF',
        'O2 QUAN - AUDIO=>OFF',
        'O2 EMER - AUDIO=>OFF',
        'EXCESS SUIT H2O - AUDIO=>OFF',
        'EXCESS CABIN H2O - AUDIO=>OFF',
        'FUEL QUAN - AUDIO=>OFF',
        'RETRO WARN - AUDIO=>OFF',
        'RETRO RESET - AUDIO=>OFF'
        ]

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
    elif eventName in WarnAudioToneEvents:
        processWarnAudioEvent(eventName, tone=True)
    elif eventName in WarnAudioOffEvents:
        processWarnAudioEvent(eventName, tone=False)
    elif eventName == 'INLET VALVE PWR=>BYPASS':
        setLight('ABORT', True)
    elif eventName == 'INLET VALVE PWR=>NORM':
        setLight('ABORT', False)
    elif eventName == 'ISOL BTRY=>STBY':
        setLight('STBY AC-AUTO', True)
    elif eventName == 'ISOL BTRY=>NORM':
        setLight('STBY AC-AUTO', False)
    elif eventName == 'TIME ZERO=>pressed':
        initiateSequencer()
    else:
        print '*** WARNING: Unhandled event name: ' + eventName

def lightTest(on):
    ''' Turn on or off all lights '''
    message = { 'type': 'LOGICAL', 'target': 'all', 'action': 'off', 'intensity': Intensity }
    if on:
        message['action'] = 'on'

    sendLightCommand(message)

def setWarnLightsBrightness(bright):
    ''' Set the brightness of the main panel warning lights to DIM or BRIGHT for lights already on '''
    global WarnIntensity

    if bright:
        WarnIntensity = BRIGHT
    else:
        WarnIntensity = DIM

    for target in WarnLightsState.keys():
        if WarnLightsState[target]:
            message = { 'type': 'LOGICAL', 'target': target, 'action': 'on', 'intensity': WarnIntensity }
            sendLightCommand(message)

def processWarnAudioEvent(eventName, tone):
    lightLabel = eventName.split(' - ')[0]
    message = { 'type': 'LOGICAL', 'target': lightLabel, 'action': 'off', 'intensity': WarnIntensity }
    if tone:
        message['action'] = 'on'
        WarnLightsState[lightLabel] = True
    else:
        WarnLightsState[lightLabel] = False

    sendLightCommand(message)

def initiateSequencer():
    sequenceLights = [
            'RETRO SEQ',
            'RETRO ATT',
            'FIRE RETRO',
            'JETT RETRO',
            'RETRACT SCOPE',
            '.05G',
            'MAIN',
            'LANDING BAG',
            'RESCUE'
            ]
    for light in sequenceLights:
        setSequenceLight(light, 'red')
        sleep(1)
        setSequenceLight(light, 'off')
        setSequenceLight(light, 'green')
        sleep(1)

def setSequenceLight(light, color):
    message = { 'type': 'LOGICAL', 'target': light, 'action': 'off', 'intensity': Intensity }
    if color != 'off':
        message['action'] = 'on'
        message['subtarget'] = color

    sendLightCommand(message)

def setLight(light, state):
    message = { 'type': 'LOGICAL', 'target': light, 'action': 'off', 'intensity': Intensity }
    if state:
        message['action'] = 'on'

    sendLightCommand(message)

def sendLightCommand(message):
    ''' Send a command to the lights controller FIFO '''
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