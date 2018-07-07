######################################################################
# testswitches.py
# Simple test utility to test the function of each switch
# Can also use: python -m evdev.evtest
######################################################################

import evdev
from select import select
from switch_info import getSwitchInfo, printSwitchInfo

def handleEvent(key, state, timestamp):
    '''
    key is a byte that represents which key/switch generated the event
    state is 0 for up, 1, for down, 2 for hold
    timestamp is time of the event as a float
    '''

    states = ('UP', 'DOWN', 'HOLD')
    if state < 2:
        print '%f %d %s' % (timestamp, key, states[state])
        printSwitchInfo(key)

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

def eventLoop():
    # A mapping of file descriptors (integers) to InputDevice instances.
    devices = map(evdev.InputDevice, ('/dev/input/event0', '/dev/input/event1', '/dev/input/event2', '/dev/input/event3'))
    devices = {dev.fd: dev for dev in devices}

    print('\nEvent wait loop started...\n')
    while True:
        r, w, x = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if event.type == evdev.ecodes.EV_KEY:
                    e = evdev.categorize(event)
                    handleEvent(e.scancode, e.keystate, event.timestamp())


################
# Main
################

showDevices()

eventLoop()

