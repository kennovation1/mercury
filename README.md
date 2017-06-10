ssh pi@192.168.1.12
raspberry

```
# Needed for I2C for servo control
# These seem to have already been installed
sudo apt-get install python-smbus 
sudo apt-get install i2c-tools
```

* sudo raspi-config 
* Use advanced options to
  * Set hostname to: rpi-mercury-1 (change in static router config too)
  * Enabled I2C
* Reboot

```
sudo i2cdetect -y 1
```

* Ground of servo goes to board edge. Ground will be brown or black.

```
git clone -b legacy https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
cd Adafruit-Raspberry-Pi-Python-Code
cd Adafruit_PWM_Servo_Driver
sudo python Servo_Example.py

sudo python kentest.py
```

* See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi for information about the PWM controller
Basically set the frequency of the Hat at 40 to 1000 Hz. Don't go crazy high since pulse rise may not hit VCC before the next pulse.
I might consider stagering the start tick of the pulses based on the channel to avoid current spikes.
When setting the value for a channel, set the start tick and end tick (0-4095). The actual width is based on the frequency. 
That is, one tick is 1/4096 * 1/freq.

In practice, each guage will need to be manually calibrated. My SG92R micro servo swings 0-180 with a width of 100 to 600 ticks 
(tested at 60 Hz).

# Setting up for Ultimarc boards

## PacLED64
* Plug in Ultimarc PacLED64
* lsusb -v and expect to find in the output:
  * idVendor           0xd209 Ultimarc
  * idProduct          0x1401
* Connect anode (positive, longer lead) of all LEDs to + on board
* Connect cathode (negative, shorter lead, flat side) of each LED to a numbered (1-64) pin on board. No resistor is required. LEDs are driven with a constant 20mA
* Supply +12VDC for LEDs at barrel connector. A HDD connector is provided to supply power. The pinout is:
  * 1 - yellow: +12V
  * 2 - black:  gnd
  * 3 - black:  gnd
  * 4 - red:    +5V
  * Note that the connector provided by Ultimarc was miswired and was using pins 3 and 4 instead of 1 and 2. I corrected the connector.
* Power up default (i.e., before any command is given) will wave the LEDs
* Linux SDK: http://katiesnow.webs.com/
* Corresponding github link: https://github.com/katie-snow/Ultimarc-linux

Connected 2 LEDs in parallel and they look good and bright but not as bright as indidually. This makes since since the PacLED64 is giving constant current, but with parallel LEDs they each only get half.
On voltage is 2.04V and 24.2mA through a single amber LED.
```
mkdir mercury
cd mercury
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

Should have done this earler...
sudo apt-get update
sudo apt-get dist-upgrade
```

Instead of using the C library above, just write my own Python code. See pacled64.py.

# Git
git init
git add README.md 
git commit -m "Initial commit"
git remote add origin git@github.com:kennovation1/mercury.git
git push -u origin master

