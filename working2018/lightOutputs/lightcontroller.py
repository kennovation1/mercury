'''
File: lightcontroller.py

Listen for light control commands from a named pipe (fifo) and set output LED state accordingly.

Usage: python lightcontroller.py &

Author: Ken Robbins
'''

import json
import os
import errno
import pacled64

LightInfo = {
            # Main panel
            'CABIN PRESS':      {'left': 16, 'right': 1},
            'O2 QUAN':          {'left': 17, 'right': 2},
            'O2 EMER':          {'left': 18, 'right': 3},
            'EXCESS SUIT H2O':  {'left': 4, 'right': 19},
            'EXCESS CABIN H2O': {'left': 5, 'right': 20},
            'FUEL QUAN':        {'left': 6, 'right': 21},
            'RETRO WARN':       {'left': 7, 'right': 22},
            'RETRO RESET':      {'left': 8, 'right': 23},
            'STBY AC-AUTO':     {'left': 24, 'right': 9},

            # Left panel
            'ABORT':         {'center': 36},
            'JETT TOWER':    {'left': 48, 'right': 63,  'center': 47},
            'SEP CAPSULE':   {'left': 61, 'right': 62, 'center': 64 },
            'RETRO SEQ':     {'left': 45, 'right': 60, 'center': 59 },
            'RETRO ATT':     {'left': 44, 'right': 58, 'center': 43 },
            'FIRE RETRO':    {'left': 42, 'right': 57, 'center': 41 },
            'JETT RETRO':    {'left': 40, 'right': 56, 'center': 55 },
            'RETRACT SCOPE': {'left': 39, 'right': 53, 'center': 54 },
            '.05G':          {'left': 37, 'right': 52, 'center': 38 },
            'MAIN':          {'left': 49, 'right': 51, 'center': 50 },
            'LANDING BAG':   {'left': 35, 'right': 46, 'center': 34 },
            'RESCUE':        {'left': 31, 'right': 33, 'center': 32 }
        }


def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise

def route(command):
    cmdType = command.get('type', 'MISSING_type')

    if cmdType == 'LOGICAL':
        handleLogical(command)
    elif cmdType == 'PHYSICAL':
        handlePhysical(command)
    elif cmdType  == 'GROUP':
        handlePattern(command)
    elif cmdType  == 'SETTINGS':
        handleSettings(command)
    else:
        print '*** ERROR: Received unknown command: ' + cmdType
        print json.dumps(command, indent=4)

def handleLogical(command):
    '''
    Control a light based on logical addressing.
    'target' the name of an indicator
    'subtarget' is a modifier. One of: 'left', 'right', 'red', 'green', 'center'
    'action' is 'on' or 'off'
    'intensity' is an integer in the range of 0 to 255. 50 seems to be a good value for Mercury
    'flashrate' is the rate to flash the LED. Integer values are: 0:no flash, 1:2secs, 2:1sec, 3:0.5secs
    '''
    if command['action'] == 'on':
        intensity = command['intensity']
    else:
        intensity = 0
    flashrate = command.get('flashrate')
    subtarget = command.get('subtarget')

    target = command.get('target', 'MISSING_TARGET')

    if target == 'all':
        Pl.setLEDIntensity('ALL', intensity, board=1)
        if flashrate is not None:
            Pl.setLEDFlash('ALL', flashrate, board=1)
    else:
        pinlist = mapLogicalToPhysical(target, subtarget)
        for pin in pinlist:
            Pl.setLEDIntensity(pin, intensity, board=1)
            if flashrate is not None:
                Pl.setLEDFlash(pin, flashrate, board=1)

def handlePhysical(command):
    '''
    Control a light based on physical addressing.
    'target' is an integer from 1 to 64 representing a PACLED64 output pin, 0 means all pins
    'action' is 'on' or 'off'
    'intensity' is an integer in the range of 0 to 255. 50 seems to be a good value for Mercury
    'flashrate' is the rate to flash the LED. Integer values are: 0:no flash, 1:2secs, 2:1sec, 3:0.5secs
    '''
    if command['action'] == 'on':
        intensity = command['intensity']
    else:
        intensity = 0

    target = command.get('target', 0)
    if target == 0:
        target = 'ALL'
    flashrate = command.get('flashrate', 0)

    Pl.setLEDIntensity(target, intensity, board=1)
    Pl.setLEDFlash(target, flashrate, board=1)

def handlePattern(command):
    '''
    Control as set of lights as a group.
    Patterns: ALL_ON, ALL_OFF, EVEN_ONLY, ODD_ONLY
    '''
    pattern = command['pattern']
    intensity = command['intensity']
    Pl.setLEDPattern(pattern, intensity, board=1)

def handleSettings(command):
    '''
    Set global settings
    Set the off/on LED ramp speed (in tens of milliseconds)
    '''
    action = command['action']
    speed = command.get('speed', 250)
    if action == 'rampspeed':
        Pl.setRampSpeed(speed, board=1)

def mapLogicalToPhysical(target, subtarget):
    ''' Returns a list of pins representing the logical label '''
    pins = []

    info = LightInfo.get(target)
    if info is None:
        return []

    if subtarget == 'left':
        pins.append(info['left'])
    elif subtarget == 'right':
        pins.append(info['right'])
    elif subtarget == 'center':
        pins.append(info['center'])
    elif subtarget == 'green':
        pins.append(info['center'])
    elif subtarget == 'red':
        pins.append(info['left'])
        pins.append(info['right'])
    elif subtarget == 'amber':
        pins.append(info['left'])
        pins.append(info['right'])
    else:
        for key in info.keys():
            pins.append(info[key])

    return pins


############
# Main
############

FIFO = '/tmp/light-commands'

makeFifo(FIFO)

Pl = pacled64.PacLED(dryRun=False)
Pl.initializeAllPacLEDs()
Pl.setLEDIntensity('ALL', 0, board=1)

# Open will block until there is a writer and a message is written
with open(FIFO, 'r') as fp:
    while True:
        # This does not block. Will return 0 if nothing to read
        mesg = fp.readline()
        if len(mesg) > 0:
            command = json.loads(mesg)
            route(command)
        else:
            # Could go off and do other things here...
            pass


