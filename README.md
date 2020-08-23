# Status
- ***See the ./working2018 sub-directory for a clean and more organized re-start of the project***

# Raspbian updates
sudo apt-get update
sudo apt-get dist-upgrade

# Connection info
ssh pi@192.168.1.12
See LastPass for password

# All else...
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
  * Enabled SPI (for experimenting with PaPiRus eInk display)
* Reboot

```
# The following was executed to test the PaPiRus eInk display. This is not normally needed since
# I don't expect to use the display.
apt-get install git -y
apt-get install python-imaging -y
apt-get install python-smbus -y
apt-get install bc i2c-tools -y

# enable SPI and I2C
raspi-config nonint do_spi 0
raspi-config nonint do_i2c 0

# For eInk testing (not needed for Mercury)
git clone https://github.com/PiSupply/PaPiRus.git
cd PaPiRus
python setup.py install    # Install PaPirRus python library

sudo pip install pypng
sudo pip install pyqrcode
```

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

# Git
```
#Put this in .bashrc?
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Common commands
git init
git add README.md 
git commit -m "Initial commit"
git remote add origin git@github.com:kennovation1/mercury.git
git push -u origin master
```

# Installing Python 3.8.5
- This failed multiple times following different approaches.
- The most recent attempt came from: https://installvirtual.com/install-python-3-8-1-on-raspberry-pi-raspbian/
  - This failed with an OpenSSL error, but was fixed by adding an extra dependencies install line
- Here the history from the final version that worked:
```
sudo apt-get update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
source .bashrc 
pyenv
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
pyenv install 3.8.5
```

Actually, that's not the full story. pyenv did not seem to be working right so I did the following
- rm -rf ~/.pyenv  # To remove old attemp of pyenv and python build
- curl https://pyenv.run | bash  # To install pyenv with some key packages
- pyenv install 3.8.5  # To build Python 3.8.5
- Now pyenv and Python seem to be installed properly.
- *HOWEVER* when I use pyenv local 3.8.5 or pyenv local gauges (after running pyenv virtualenv 3.8.5 gauges)
  and run python -V it points to /usr/bin/python which though pyenv which python shows a correct path.
  .pyenv is at the start of the path. I'm stumped for the moment.
- This seems to have been the missing step:
  - echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  - The restart shell

## Python version selection
- pyenv versions
- cd to dir for project that needs 3.x and run:
  - pyenv local 3.8.5
  - This sets the version just for the local directory
  - See pyenv doc for other ways to set versions locally and globally
    - https://realpython.com/intro-to-pyenv/
- Better yet
  - pyenv virtualenv 3.8.5 gauges  # From in the gauges dir
  - pyenv local guages 3.8.5  # To activate the virtual env

# Install websockets
- Make sure to be in the current pyenv/virtualenv
- pip install websockets
- pip install flask  # Was briefly used to verify network access. Not really needed for now.

# Install apache2
- sudo apt update
- sudo apt install apache2 -y
- Files in /var/www/html/

