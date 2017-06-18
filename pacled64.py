'''
File: pacled64.py

Utility to control an Ultimarc PacLED64.

This is not written for general use, but can readily be modified.
At present, this is focused on my Mercury capsule project.
My use case is to control a single PacLED64 on a single USB bus.
The devices were ordered with no changes to default settings (unlike how my PacDrives were ordered)
This is meant to work on a Raspberry PI 3 model B and is not generalized beyond that.

See README.md for wiring notes (perhaps move/copy to here in the future).

Author: Ken Robbins

Thanks to Robert Abram and Katie Snow (Ultimarc-linux) whose source code provided insight into PacLED64
programming and for their #define values for PACLED*

Command interface design (see separate spreadsheet for full command set):
Function                            high byte map[0]    low byte map[1]
----------------------------------  -----------------   ----------------
Set one LED to given intensity      LED num             intensity value
Set all LEDs to given intensity     0x80                intensity value
Set all LEDs to random full on/off  0x89                0
Set flash rate for all LEDs         0x40                flash rate + PACLED_FADE_ALL_BASE
Set flash rate for one LED          LED num +           flash rate
                                    PACLED_FADE_BASE
Set off/on ramp speed               0xC0                tens of milliseconds
Update board ID                     0xFE                newId + 240 (only needed if multiple boards)

LED num: 0-63
Flash rate: 0-3  (0:no flash, 1:2secs, 2:1sec, 3:0.5secs)
intensity: 0-255
PACLED_FADE_BASE: 64
PACLED_FADE_ALL_BASE: 4

When an LED is turned on, it remains on until intensity is set to a different
level (or 0) or the flash rate is changed.

Changing the flash rate takes effect immediately. So, if an LED is solid on or flashing at some rate,
issuing the command will start flashing the LED at the new rate. However, if you set rate
to 0, when the LED is in the off state, then it stays off. If it was on, then it stays on.

The 'FADE' term in the constants above (borrowed from Katie Snow) is confusing but works (I would have thought
it would be called FLASH. Also, there is a way to set the fade time globally, but I don't yet know that command.
'''
import usb.core
import usb.util
import unittest
import logging
from time import sleep

# USB constants
PACLED_VENDOR = 0xD209
PACLED_PRODUCT = 0x1401 # This may not be true for multiple boards (next might be 1402, etc.)
PACLED_DATA_SIZE = 2
PACLED_REPORT = 0x03
PACLED_VALUE = 0x0200
PACLED_INDEX = 0
PACLED_MESG_LENGTH = 2
PACLED_INTERFACE = 0
PACLED_FADE_BASE = 64
PACLED_FADE_ALL_BASE = 4

UM_REQUEST_TYPE = 0x21
UM_REQUEST = 9

# PacDrive characteristics
PACLED_LEDS = 64
MAX_BOARDS = 1      # Code not tested for >1

'''
Class represents a set of PacLED boards and their LED controls.
Boards are numbered starting at 1.
LEDs are numbered starting at 1 as marked on PacLED silkscreen (note that commands to board are 0-based).

Commands are directly written to the board (no local state is maintained).
'''
class PacLED:
    def __init__(self, dryRun=False):
        self.dryRun = dryRun

    def initializeAllPacLEDs(self):
        '''
        Iterate over all USB-attached PacLEDs that are found and intialize each
        '''
        self.devs = []
        if self.dryRun:
            for i in range(1, MAX_BOARDS+1):
                self.devs.append('Dummy device ' + str(i))
	    return

        devsIter = usb.core.find(idVendor=PACLED_VENDOR, idProduct=PACLED_PRODUCT, find_all=True)
        if devsIter is None:
	    raise ValueError('No PacLED devices found')

        for dev in devsIter: # Can only read this iter once
	    if dev.is_kernel_driver_active(0): # Okay to hardcode 0?
	        dev.detach_kernel_driver(0)
	    dev.set_configuration() # Assumes that the default is the right one
	    self.devs.append(dev)

    def setLEDIntensity(self, LED, intensity, board=1):
        '''
        Given a board (1-4) and an LED number (1-64), set the intensity (0-255)
        where 0 is off and 255 is full brightness.
        If LED is 'ALL', apply to all LEDs on board.
        '''
        msg = [0,0]
        if LED is 'ALL':
            msg[0] = 0x80
        else:
            msg[0] = LED-1

        msg[1] = intensity

        self.sendCommand(board, msg)

    def setLEDFlash(self, LED, rate, board=1):
        '''
        Given a board (1-4) and an LED number (1-64), set the flash rate (0-3).
        If LED is 'ALL', apply to all LEDs on board.
        Flash rate: 0-3  (0:no flash, 1:2secs, 2:1sec, 3:0.5secs)
        Setting the flash rate immediately affects the current state. Also, if setting to 0 (no flash),
        then the state will stick to on or off depending on the state at the instant the command was given.
        '''
        msg = [0,0]
        if LED is 'ALL':
            msg[0] = 0x40
            msg[1] = rate + PACLED_FADE_ALL_BASE
        else:
            msg[0] = LED-1 + PACLED_FADE_BASE
            msg[1] = rate

        self.sendCommand(board, msg)

    def setLEDRandom(self, board=1):
        ''' Set all LEDs to a random full on/off pattern on the specified board'''
        msg = [0,0]
        msg[0] = 0x89
        msg[1] = 0
        self.sendCommand(board, msg)

    def setRampSpeed(self, speed, board=1):
        ''' Set the off/on LED ramp speed (in tens of milliseconds) on the specified board '''
        msg = [0,0]
        msg[0] = 0xC0
        msg[1] = speed
        self.sendCommand(board, msg)

    def setLEDPattern(self, pattern, intensity, board=1):
        ''' Set the output state according to a pattern command '''
        self.setLEDIntensity('ALL', 0, board) # First, turn off all LEDs

        if pattern == 'ALL_ON':
            self.setLEDIntensity('ALL', intensity, board)
        elif pattern == 'EVEN_ONLY':
            for i in range(2, PACLED_LEDS+1, 2):
                self.setLEDIntensity(i, intensity, board)
        elif pattern == 'ODD_ONLY':
            for i in range(1, PACLED_LEDS, 2):
                self.setLEDIntensity(i, intensity, board)
        else: # 'ALL_OFF'
            self.setLEDIntensity('ALL', 0, board)

    def sendCommand(self, board, msg):
        ''' Send a command to an attached PacLED. board is in range 1-N. '''
        if self.dryRun:
            print 'dryRun: 0x%02x 0x%02x' % (msg[0], msg[1])
        else:
            assert self.devs[board-1].ctrl_transfer(UM_REQUEST_TYPE, UM_REQUEST, PACLED_VALUE, PACLED_INDEX, msg) == PACLED_MESG_LENGTH

# End class PacLED

# Utility functions:

def mapLogicalIdToBoardAndLED(logicalId):
    '''
    Maps a logical ID in the range of 1 to 256 to a board ID (1-4)
    and a LED number (1-64). Note that the logical LED number is given.
    Returns a tuple (boardId, LED)
    '''
    boardId = ((logicalId-1) / PACLED_LEDS) + 1
    LED  = ((logicalId-1) % PACLED_LEDS)
    return (boardId, LED+1)

def mapLabelToBoardAndLED(label):
    '''
    Map a text label for a LED to the board and LED number that is wired to that LED
    Returns a tuple (boardId, LED). The returned LED number is a logical 1-64 number to
    match board silkscren.
    '''
    labelMap = {
            'led1': (1,1),
            'led2': (1,2),
            'led3': (1,3),
            'led4': (1,4),
            'led5': (1,5),
            'led6': (1,6),
            'led7': (1,7),
            'led8': (1,8),
            'led9': (1,9),
            'led10': (1,10),
            'led11': (1,11),
            'led12': (1,12),
            'led13': (1,13),
            'led14': (1,14),
            'led15': (1,15),
            'led16': (1,16),
            'led17': (1,17),
            'led18': (1,18),
            'led19': (1,19),
            'led20': (1,20),
            'led21': (1,21),
            'led22': (1,22),
            'led23': (1,23),
            'led24': (1,24),
            'led25': (1,25),
            'led26': (1,26),
            'led27': (1,27),
            'led28': (1,28),
            'led29': (1,29),
            'led30': (1,30),
            'led31': (1,31),
            'led32': (1,32),
            'led33': (1,33),
            'led34': (1,34),
            'led35': (1,35),
            'led36': (1,36),
            'led37': (1,37),
            'led38': (1,38),
            'led39': (1,39),
            'led40': (1,40),
            'led41': (1,41),
            'led42': (1,42),
            'led43': (1,43),
            'led44': (1,44),
            'led45': (1,45),
            'led46': (1,46),
            'led47': (1,47),
            'led48': (1,48),
            'led49': (1,49),
            'led50': (1,50),
            'led51': (1,51),
            'led52': (1,52),
            'led53': (1,53),
            'led54': (1,54),
            'led55': (1,55),
            'led56': (1,56),
            'led57': (1,57),
            'led58': (1,58),
            'led59': (1,59),
            'led60': (1,60),
            'led61': (1,61),
            'led62': (1,62),
            'led63': (1,63),
            'led64': (1,64)
            }
    return labelMap[label]


#############
# unittests #
#############
class TestController(unittest.TestCase):
    def setUp(self):
        self.dryRun = False
        self.delay = 2 # Seconds to hold test to allow visual inspection

    @unittest.skip('Only run this if I change mapLogicalIdToBoardAndLED')
    def test_mapLogicalIdToBoardAndLED(self):
        print '\nTest of mapLogicalIdToBoardAndLED'
        # A few tests, but mostly just need to read the output when changing the code
        for logicalId in range(1,129):
            (boardId, LED) = mapLogicalIdToBoardAndLED(logicalId)
            print '%d\t%d\t%d' % (logicalId, boardId, LED)
        self.assertEqual(logicalId, 128, 'Unexpected logicalId value')
        self.assertEqual(boardId, 2, 'Unexpected boardId value')
        self.assertEqual(LED, 64, 'Unexpected LED value')

    @unittest.skip('Only run this if I change mapLabelToBoardAndLED')
    def test_mapLabelToBoardAndLED(self):
        # A few tests, but mostly just need to read the output when changing the code
        print '\nTest of mapLabelToBoardAndLED'
        (boardId, LED) = mapLabelToBoardAndLED('led1')
        print '%s\t%d\t%d' % ('led1', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('led2')
        print '%s\t%d\t%d' % ('led2', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('led64')
        print '%s\t%d\t%d' % ('led64', boardId, LED)
        self.assertEqual(boardId, 1, 'Unexpected boardId value')
        self.assertEqual(LED, 64, 'Unexpected boardId value')

    def test_initializeAllPacDrives(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        self.assertEqual(len(pl.devs), MAX_BOARDS, 'Wrong number of PacLEDs found')

        # TODO: Do I need to do this anywhere?
        # for dev in pl.devs:
        #    usb.util.dispose_resources(dev)

    def test_setLEDIntensityRamp(self):
        print '\nVisually verify that LED intensity ramps from LED 1 as dimmest to LED 64 as brightest\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        for LED in range(1, 65):
            pl.setLEDIntensity(LED, (LED)*4 - 1)
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDFlash(self):
        print '\nVisually verify that all LEDs light and then flash at diff rates (every 4)\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDFlash('ALL', 0)
        pl.setLEDIntensity('ALL', 255)
        for LED in range(1, 65, 4):
            for i in range(0, 4):
                pl.setLEDFlash(LED+i, i)
        sleep(2 * self.delay)
        pl.setLEDFlash('ALL', 0)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDIntensityAll(self):
        print '\nVisually verify that all LEDs are at max intensity\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDIntensity('ALL', 255)
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setRampSpeed(self):
        print '\nVisually verify that all LEDs turn on very slowly (2 secs) and off fast (0.25 secs)\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setRampSpeed(200) # 2 seconds
        pl.setLEDIntensity('ALL', 255)
        sleep(self.delay)
        pl.setRampSpeed(25)  # 0.5 seconds
        pl.setLEDIntensity('ALL', 0)
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDFlashAll(self):
        print '\nVisually verify that all LEDs flash at same rate\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDIntensity('ALL', 255)
        for rate in range(4):
            print '\tRate:', rate
            pl.setLEDFlash('ALL', rate)
            sleep(2*self.delay)
        pl.setLEDFlash('ALL', 0)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDPattern(self):
        print '\nVisually verify that all LEDs went to...\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        intensity = 64
        for pattern in ('ALL_ON', 'EVEN_ONLY', 'ODD_ONLY', 'ALL_OFF'):
            print '\t' + pattern + '\n'
            pl.setLEDPattern(pattern, intensity)
            intensity += 64
            sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDRandom(self):
        print '\nVisually verify that board is in random mode\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDRandom()
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')


########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACLED:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.DEBUG
    #logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    unittest.main()

# TODO:
# Create utility to set a pattern, delay and then set another pattern until list of patterns is complete
# and then start over or end.
