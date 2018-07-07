# Switch Inputs
This directory contains code to read the switch inputs from the Mercury instrument panels.
An Ultimarc IPAC-4 device is used to read the switch state. The IPAC-4 detects switch closures and reports them as
key press events via USB.

Events are generated for key up, key down, and key hold.
Note that the IPAC-4 reports events and cannot poll for current state per se.
However, if a switch is closed (key down) then a stream of 'hold' events flows.
But, only the last key in the hold position will be reported. So if switch A is closed it will report a stream
That is, if a hold stream is being sent from one switch, the next event will stop the hold stream.
of holds. Then if switch B is closed, it will report a stream of holds, but A will not longer send hold events.

Emprically:
A hold event will be delivered if the key is down for about 240ms
Hold events are spaced at a 40ms interval when called in a tight loop on one input device.

# Status
- **Ground is not cabled yet. Need to use aligator clip**
- Switches that are wired generally seem to work. Need to map out and test each.
- testswithches.py: I need to handle reading all four devices at once

# Setup

## evdev
- [edev doc](https://python-evdev.readthedocs.io/en/latest/) "python-evdev allows you to read and write input events on Linux. An event can be a key or button press, a mouse movement or a tap on a touchscreen."
- sudo pip install evdev
  - On 7/7/2018 I ran: sudo pip install evdev . This increased version from 0.7.0 to 1.0.0
- I had originally tried to use pyusb to read the IPAC-4 but got a "Resource Busy" error. This is why I moved to evdev.


