# Setup and configuration of Ultimarc PacLED64

## Software configuration
- Plug in Ultimarc PacLED64
- lsusb -v and expect to find in the output:
  - idVendor           0xd209 Ultimarc
  - idProduct          0x1401
- Power up default (i.e., before any command is given) will wave the LEDs
- References:
  - Linux SDK: http://katiesnow.webs.com/
  - Corresponding github link: https://github.com/katie-snow/Ultimarc-linux
### Linux tools
- The following has not been reviewed for a while. It's possible that there may be updates.
- Instead of trying to use the Katie Snow C library, just write my own Python code. See pacled64.py.
```
git clone https://github.com/katie-snow/Ultimarc-linux.git
cd Ultimarc-linux
sudo apt-get install libjson0 libjson0-dev
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install autoconf autogen intltool
./autogen.sh
./configure
make

sudo cp 21-ultimmarc.rules /etc/udev/rules.d/
sudo reboot
lsusb
sudo lsusb -v

cd src/umtool
./umtool pacLED.json
```

## Hardware wiring
- Connect anode (positive, longer lead) of all LEDs to + on board
- Connect cathode (negative, shorter lead, flat side) of each LED to a numbered (1-64) pin on board.
- No resistor is required. LEDs are driven with a constant 20mA

### Question this!
- **I think this should really be just +5VDC not +12VDC as previously noted; check emails from Andy at Ultimarc**
- Supply voltate for LEDs at barrel connector. A HDD connector is provided to supply power. The pinout is:
  - 1 - yellow: +12V
  - 2 - black:  gnd
  - 3 - black:  gnd
  - 4 - red:    +5V
  - Note that the connector provided by Ultimarc was miswired and was using pins 3 and 4 instead of 1 and 2. I corrected the connector. **Was this correct or did I overthink something?**

As an experiment, I connected 2 LEDs in parallel and they look good and bright but not as bright as indidually.
This makes since since the PacLED64 is giving constant current, but with parallel LEDs they each only get half.
Therefore, I stuck with wiring individually for Telelights that have two greens for example.
On voltage was measured at 2.04V and 24.2mA through a single amber LED.

# TODO
- Ramp speed only affects all???
- For pacLED, until I get a working board, block bad LEDS in software since I seem to be burning out the driver board
  when I drive the bad LED ports.

# Usage
- python testui.py # To get interactive session to control LEDS
  - Right/main panel telelights are 1-9 (top to bottom)
  - Left panel telelights are 10-19 (**don't use 10 and 11 for now**)
  - Abort is pin 36
