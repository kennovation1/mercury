from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event1')

import evdev
'''
key_up = 0
key_down = 1
key_hold = 2
print evdev.events.KeyEvent.key_up
'''

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print event
        e = categorize(event)
        print e
        print e.keycode
        print e.keystate
        print e.scancode
