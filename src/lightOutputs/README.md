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
- Use **5VDC** supply to barrel connector. Ignore the silksreen that says +12V. Current supply is 4A which should be
  plenty. 64 LEDs times 20ma is 1.28A, the minumum required.

As an experiment, I connected 2 LEDs in parallel and they look good and bright but not as bright as indidually.
This makes since since the PacLED64 is giving constant current, but with parallel LEDs they each only get half.
Therefore, I stuck with wiring individually for Telelights that have two greens for example.
On voltage was measured at 2.04V and 24.2mA through a single amber LED.

# Status
- All lights work
- Intensity 50 seems good

# TODO
- Confirm that ramp speed only affects all and cannot be set of an individual LED
- Until I get a working board or work around bad pins, block bad LEDS in software since I seem to be burning out
  the driver board when I drive the bad LED ports.
- Updgrade Ultimarc Linux SW?
- Consider creating a boot script if easy to do

# Usage for UI testing
- python testui.py # To get interactive session to control LEDs
  - Right/main panel telelights are 1-9 (top to bottom)
  - Left panel telelights are 10-19 (**don't use 10 and 11 for now**)
  - Abort is pin 36

# Normal usage
- python lightcontroller.py &
- This listens for commands on named pipe (FIFO)
