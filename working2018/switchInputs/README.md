# Switch Inputs
This directory contains code to read the switch inputs from the Mercury instrument panels.
An Ultimarc IPAC-4 device is used to read the switch state. The IPAC-4 detects switch closures and reports them as
key press events via USB.

# IPAC-4
- [IPAC-4 product info](https://www.ultimarc.com/ipac1.html)
- 56 inputs

Events are generated for key up, key down, and key hold.
Note that the IPAC-4 reports events and cannot poll for current state per se.
However, if a switch is closed (key down) then a stream of 'hold' events flows.
But, only the last key in the hold position will be reported. So if switch A is closed it will report a stream
That is, if a hold stream is being sent from one switch, the next event will stop the hold stream.
of holds. Then if switch B is closed, it will report a stream of holds, but A will not longer send hold events.

Emprically:
A hold event will be delivered if the key is down for about 240ms
Hold events are spaced at a 40ms interval when called in a tight loop on one input device.

I used `umtool mercury.json` to remap the keys. This was required since the factory settings has a bunch of pins
mapped to space and not unique values. Also, ther are two shift keys that behave differently and I don't want to use
(might be able to use for momementary buttons). I mapped these to 1COIN and 2COIN respectively and have not wired
anything to those pins.

umtool was build separately and the binary copied into this directory.

See `ipac4-mercury.json` for the mapping. This should also match switch_info.py
See Ultimarc-linux directory for the source for umtool and how to build and run it.

# Status
- TODO Update switch_info.py to match ipac4-mercury.json mappings
- TODO **Ground is not cabled yet. Need to use aligator clip**
- Don't use 1COIN or 2COIN (maybe use for momentary if needed). These are shift buttons and only sent events
  when the key state is UP (and then sends both the DOWN and UP events).
- All switches that are wired work
- Still need to wire:
  - All momentary switches
  - VOX PWR
  - UHF DF
  - STBY BTRY
  - All left side brown and tan panel toggles
  - Fuel control values and pull pins

# Setup
- Connect to Pi with USB-to-micro-USB cable
- No separate power required
- Short signal to ground for a keydown event. That is, closing a switch closes circuit between signal pin and ground and generates a key down event.

## evdev
- [edev doc](https://python-evdev.readthedocs.io/en/latest/) "python-evdev allows you to read and write input events on Linux. An event can be a key or button press, a mouse movement or a tap on a touchscreen."
- sudo pip install evdev
- I had originally tried to use pyusb to read the IPAC-4 but got a "Resource Busy" error. This is why I moved to evdev.

# Testing
- python fiforecv.py & # To receive events and print to screen if -f switch is used below; or
- python fiforecv.py > /dev/null & # To consume events, but don't display debug output (or redirect to a file)
- python readswitches.py [-f]
  - Toggle buttons and observe printout to screen for each state change. Continuous hold events are not printed.
  - -f is optional and will cause events to be written to fifo that can be read by fiforecv.py

