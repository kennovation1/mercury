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

Downloaded and run MacIPAC to use UI to set key mappings (since umtool seems to do nothing).
__2COIN and 4COIN__ are set to be the shift keys. Don't use these for toggles since the down event is not sent
until the up event is sent.

See Ultimarc-linux directory for the source for umtool and how to build and run it. *HOWEVER*, this seems not to work.
I ran the tool and it said success, but it didn't seem to change the board configuration. This is why I used
MacIPAC UI instead.

# Status
- All switches main panel switches work
- Not wired: All left panel panel toggles, fuel control values and pull pins

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

# Usage
- python readswitches.py -f &
- Sends switch state events to named pipe (FIFO). Skip writing to pipe by omitting -f for debugging
