######################################################################
# readswitches.py
# Simple test utility to test the function of each switch
# Can also use: python -m evdev.evtest
######################################################################

import evdev
from select import select
from switch_info import getSwitchInfo, printSwitchInfo, makeEventMessage
import sys
import json
import os
import errno

def handleEvent(key, state, timestamp, fifo):
    '''
    key is a byte that represents which key/switch generated the event
    state is 0 for up, 1, for down, 2 for hold
    timestamp is time of the event as a float

    fifo is a file pointer to a fifo or None if not enabled
    '''

    states = ('UP', 'DOWN', 'HOLD')
    if state < 2:
        #print '%f %d %s' % (timestamp, key, states[state])
        printSwitchInfo(key, state)
        mesg = makeEventMessage(key, state)
        sendEventMessage(mesg, fifo)

def showDevices():
    print('\nDiscovered devices:')
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    if len(devices) != 4:
        print('Expected 4 input devices, but found ' + str(len(devices)))
    for device in devices:
        print(device.path, device.name, device.phys)
        if device.name != 'Ultimarc Ultimarc':
            print('    WARNING: Expected device name to be "Ultimarc Ultimarc"')
    ''' Expect printed output to be: 
        ('/dev/input/event3', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input3')
        ('/dev/input/event2', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input2')
        ('/dev/input/event1', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input1')
        ('/dev/input/event0', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input0')
    '''

def eventLoop(fifo):
    # A mapping of file descriptors (integers) to InputDevice instances.
    devices = map(evdev.InputDevice, ('/dev/input/event0', '/dev/input/event1', '/dev/input/event2', '/dev/input/event3'))
    devices = {dev.fd: dev for dev in devices}

    print('\nEvent wait loop started (control-C to stop)...\n')

    while True:
        r, w, x = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if event.type == evdev.ecodes.EV_KEY:
                    e = evdev.categorize(event)
                    handleEvent(e.scancode, e.keystate, event.timestamp(), fifo)

def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise

def sendEventMessage(mesg, fifo):
    if fifo:
        buff =  json.dumps(mesg) + '\n'
        # Newline makes it possible to use readline on the other size so that I have a good message boundary
        fifo.write(buff)
        fifo.flush()

def usage(cmd):
    print 'Usage: {} [-f]'.format(cmd)
    print '    -f: Enable writing to fifo'
    sys.exit(1)



################
# Main
################

FIFO = '/tmp/mercury-events'

# Get command line args
enableFifo = False
argCount = len(sys.argv)

if argCount > 1:
    if argCount == 2:
        if sys.argv[1] == '-f':
            enableFifo = True
        else:
            usage(sys.argv[0])
    else:
        usage(sys.argv[0])

showDevices()

fifo = None
if enableFifo:
    makeFifo(FIFO)
    # Open and writes will block if no reader on fifo (or if full)
    print '\nWaiting for reader to connect to FIFO...'
    fifo = open(FIFO, 'w')
else:
    print 'FIFO not enabled.'

eventLoop(fifo)

fifo.close()
