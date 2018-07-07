######################################################################
# testswitches.py
# Simple test utility to test the function of each switch
# Can also use: python -m evdev.evtest
######################################################################

import evdev
from time import time

def handleEvent(key, state):
    '''
    key is a byte that represents which which generated the event
    state is 0 for up, 1, for down, 2 for hold
    '''

    states = ['UP', 'DOWN', 'HOLD']
    print time(), 'Key=' + str(key) + ' State=' + states[state]

def showDevices():
    print('\nDiscovered devices:')
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    if len(devices) != 4:
        print('Expected 4 input devices, but found ' + len(devices))
    for device in devices:
        print(device.path, device.name, device.phys)
        if device.name != 'Ultimarc Ultimarc':
            print('    WARNING: Excpected device name to be "Ultimarc Ultimarc"')
    ''' Expect printed output to be: 
        ('/dev/input/event4', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input3')
        ('/dev/input/event3', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input2')
        ('/dev/input/event2', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input1')
        ('/dev/input/event1', 'Ultimarc Ultimarc', 'usb-3f980000.usb-1.3/input0')
    '''

################
# Main
################

showDevices()

def testAsync():
    from selectors import DefaultSelector, EVENT_READ
    selector = selectors.DefaultSelector()

    for i in range(1,4):
        inputDevice = evdev.InputDevice('/dev/input/event' + str(i))
        # This works because InputDevice has a `fileno()` method.
        selector.register(inputDevice, selectors.EVENT_READ)

    while True:
        for key, mask in selector.select():
            device = key.fileobj
            for event in device.read():
                print(event)


# TODO: Need to update to read from all four devices concurrently ...
device = evdev.InputDevice('/dev/input/event1')

print('\nEvent wait loop started...\n')
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        e = evdev.categorize(event)
        '''
        print event
        print e
        print e.keycode
        print e.keystate
        print e.scancode
        '''
        handleEvent(e.scancode, e.keystate)
