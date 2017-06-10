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

Command interface design:
Function                            low byte map[0]     high byte map[1]
----------------------------------  -----------------   ----------------
Set one LED to given intensity      LED num             intensity value
Set all LEDs to given intensity     0x80                intensity value
Set all LEDs in random mode         0x89                0
Fade all LEDs at given rate         0x40                fade rate + PACLED_FADE_ALL_BASE
Fade one LED at given rate          LED num +           fade rate
                                    PACLED_FADE_BASE
Update board ID                     0xFE                newId + 240

LED num: 0-63
fade rate: 0-3
intensity: 0-255
PACLED_FADE_BASE: 64
PACLED_FADE_ALL_BASE: 4

When an LED is turned on, it remains on until intensity is set to a different
level (or 0), or a fade command is issued.
'''
import usb.core
import usb.util
import unittest
import logging
from time import sleep

# USB constants
PACLED_VENDOR = 0xD209
PACLED_PRODUCT = 0x1401
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
MAX_BOARDS = 1

'''
Class represents a set of PacLED boards and their LED controls.
Boards are numbered starting at 1.

Unlike the PacDrives, no shadow state is maintained. Commands are directly
written to the board.
'''
class PacLED:
    def __init__(self, dryRun=True):
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

    def setLEDIntensityPhysical(self, board, LED, intensity):
        '''
        Given a board (1-4) and an LED number (0-63), set the intensity (0-255)
        where 0 is off and 255 is full brightness.
        'Physical' means that we are using board and LED addressing instead of a
        logical 1-256 LED namespace.
        '''
        msg = [0,0]
        if LED is 'ALL':
            msg[0] = 0x80
        else:
            msg[0] = LED & 0x00ff

        msg[1] = intensity & 0x00ff

        self.sendCommand(board, msg)

    def setLEDRandom(self, board):
        ''' Put board in random mode '''
        msg = [0,0]
        msg[0] = 0x89
        msg[1] = 0
        self.sendCommand(board, msg)

    def setLEDPattern(self, board, pattern, intensity):
        ''' Set the output state according to a pattern command '''
        self.setLEDIntensityPhysical(board, 'ALL', 0)

        if pattern == 'ALL_ON':
            self.setLEDIntensityPhysical(board, 'ALL', intensity)
        elif pattern == 'EVEN_ONLY':
            for i in range(0, PACLED_LEDS, 2):
                self.setLEDIntensityPhysical(board, i, intensity)
        elif pattern == 'ODD_ONLY':
            for i in range(1, PACLED_LEDS, 2):
                self.setLEDIntensityPhysical(board, i, intensity)
        else: # 'ALL_OFF'
            self.setLEDIntensityPhysical(board, 'ALL', 0)

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
    and a LED number (0-63)
    Returns a tuple (boardId, LED)
    '''
    boardId = ((logicalId-1) / PACLED_LEDS) + 1
    LED  = ((logicalId-1) % PACLED_LEDS)
    return (boardId, LED)

def mapLabelToBoardAndLED(label):
    '''
    Map a text label for a LED to the board and LED number that is wired to that LED
    Returns a tuple (boardId, LED)
    '''
    labelMap = {
            'sw1': (1,0),
            'sw2': (1,1),
            'sw3': (1,2),
            'sw4': (1,3),
            'sw5': (1,4),
            'sw6': (1,5),
            'sw7': (1,6),
            'sw8': (1,7),
            'sw9': (1,8),
            'sw10': (1,9),
            'sw11': (1,10),
            'sw12': (1,11),
            'sw13': (1,12),
            'sw14': (1,13),
            'sw15': (1,14),
            'sw16': (1,15),
            'sw17': (1,16),
            'sw18': (1,17),
            'sw19': (1,18),
            'sw20': (1,19),
            'sw21': (1,20),
            'sw22': (1,21),
            'sw23': (1,22),
            'sw24': (1,23),
            'sw25': (1,24),
            'sw26': (1,25),
            'sw27': (1,26),
            'sw28': (1,27),
            'sw29': (1,28),
            'sw30': (1,29),
            'sw31': (1,30),
            'sw32': (1,31),
            'sw33': (1,32),
            'sw34': (1,33),
            'sw35': (1,34),
            'sw36': (1,35),
            'sw37': (1,36),
            'sw38': (1,37),
            'sw39': (1,38),
            'sw40': (1,39),
            'sw41': (1,40),
            'sw42': (1,41),
            'sw43': (1,42),
            'sw44': (1,43),
            'sw45': (1,44),
            'sw46': (1,45),
            'sw47': (1,46),
            'sw48': (1,47),
            'sw49': (1,48),
            'sw50': (1,49),
            'sw51': (1,50),
            'sw52': (1,51),
            'sw53': (1,52),
            'sw54': (1,53),
            'sw55': (1,54),
            'sw56': (1,55),
            'sw57': (1,56),
            'sw58': (1,57),
            'sw59': (1,58),
            'sw60': (1,59),
            'sw61': (1,60),
            'sw62': (1,61),
            'sw63': (1,62),
            'sw64': (1,63)
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
        self.assertEqual(LED, 63, 'Unexpected LED value')

    @unittest.skip('Only run this if I change mapLabelToBoardAndLED')
    def test_mapLabelToBoardAndLED(self):
        # A few tests, but mostly just need to read the output when changing the code
        print '\nTest of mapLabelToBoardAndLED'
        (boardId, LED) = mapLabelToBoardAndLED('sw1')
        print '%s\t%d\t%d' % ('sw1', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('sw2')
        print '%s\t%d\t%d' % ('sw2', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('sw64')
        print '%s\t%d\t%d' % ('sw64', boardId, LED)
        self.assertEqual(boardId, 1, 'Unexpected boardId value')
        self.assertEqual(LED, 63, 'Unexpected boardId value')

    def test_initializeAllPacDrives(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        self.assertEqual(len(pl.devs), MAX_BOARDS, 'Wrong number of PacLEDs found')

        # TODO: Do I need to do this anywhere?
        # for dev in pl.devs:
        #    usb.util.dispose_resources(dev)

    def test_setLEDIntensityPhysicalRamp(self):
        print '\nVisually verify that LED intensity ramps from LED 1 as dimmest to LED 64 as brightest\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        for LED in range(0, 64):
            pl.setLEDIntensityPhysical(1, LED, (LED+1)*4 - 1)
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDIntensityPhysicalAll(self):
        print '\nVisually verify that all LEDs are at max intensity\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDIntensityPhysical(1, 'ALL', 255)
        sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDPattern(self):
        print '\nVisually verify that all LEDs went to...\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        intensity = 64
        for pattern in ('ALL_ON', 'EVEN_ONLY', 'ODD_ONLY', 'ALL_OFF'):
            print '\t' + pattern + '\n'
            pl.setLEDPattern(1, pattern, intensity)
            intensity += 64
            sleep(self.delay)
        self.assertTrue(True, 'Should never fail')

    def test_setLEDRandom(self):
        print '\nVisually verify that board is in random mode\n'
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDRandom(1)
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
