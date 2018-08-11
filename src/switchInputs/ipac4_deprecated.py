# OLD/DEPRECATED - Keep around for ideas on building a controller for the telelights, but don't use this any more
from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event1')

import evdev
import pacled64

def mapTelelightToPins(telelight):
    # As viewed from front, top to bottom, main panel
    mapping = [ (1,16), (2,17), (3,18), (19,4), (20,5), (21,6), (22,7), (23,8), (9,24) ]
    return mapping[telelight-1]

def mapSwitchCodeToTelelight(switchCode):
    switchMap = {
            36:1,
            23:2,
            37:3,
            97:4,
            54:5,
            28:6,
            24:7,
            63:8,
            64:9
            }
    return switchMap.get(switchCode, 0)

def handleEvent(key, state):
    '''
    key is a byte that represents which which generated the event
    state is 0 for up, 1, for down, 2 for hold
    '''
    states = ['UP', 'DOWN', 'HOLD']
    print 'Key=' + str(key) + ' State=' + states[state]
    '''
    Top switch: 31, left=down, right=up
    CABIN PRESS: 4, left=down, right=up
    '''
    if key == 38:
        if state == 0:
            pl.setLEDPattern('ALL_ON', 255)
        elif state == 1:
            pl.setLEDPattern('ALL_OFF', 0, )
    else:
        telelight = mapSwitchCodeToTelelight(key)
        print 'TELELIGHT:', telelight
        if telelight > 0:
            pins = mapTelelightToPins(telelight)
            for pin in pins:
                if state == 0:
                    pl.setLEDIntensity(pin, 255)
                elif state == 1:
                    pl.setLEDIntensity(pin, 0)


# Main
pl = pacled64.PacLED(dryRun=False)
pl.initializeAllPacLEDs()

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        e = categorize(event)
        '''
        print event
        print e
        print e.keycode
        print e.keystate
        print e.scancode
        '''
        handleEvent(e.scancode, e.keystate)
