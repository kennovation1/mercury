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
'''
import usb.core
import usb.util
import unittest
import logging

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
        self.devs = {}
        if self.dryRun:
            for i in range(1, MAX_BOARDS+1):
                self.devs[i] = 'Dummy device ' + str(i)
	    return

        devsIter = usb.core.find(idVendor=PACLED_VENDOR, idProduct=PACLED_PRODUCT, find_all=True)
        if devsIter is None:
	    raise ValueError('No PacLED devices found')

        for dev in devsIter: # Can only read this iter once
	    if dev.is_kernel_driver_active(0): # Okay to hardcode 0?
	        dev.detach_kernel_driver(0)
	    dev.set_configuration() # Assumes that the default is the right one
	    self.devs[dev.bcdDevice] = dev

    def setLEDIntensityPhysical(self, board, LED, intensity):
        '''
        Given a board (1-4) and an LED number (1-64), set the intensity (0-255)
        where 0 is off and 255 is full brightness.
        'Physical' means that we are using board and LED addressing instead of a
        logical 1-256 LED namespace.
        '''
        msg = {}
        if LED is 'ALL':
            msg[0] = 0x80
        else:
            msg[0] = LED & 0x00ff

        msg[1] = intensity & 0x00ff

        self.sendCommand(board, msg)


    def updatePattern(self, pattern):
        ''' Set the output state according to a pattern command '''
        # TODO: write this
        if pattern == 'ALL_ON':
            pass
        elif pattern == 'EVEN_ONLY':
            pass
        elif pattern == 'ODD_ONLY':
            pass
        else: # 'ALL_OFF'
            pass

    def sendCommand(self, board, msg):
        ''' Send a command to an attached PacLED '''
        if self.dryRun:
            print 'dryRun: 0x%02x 0x%02x' % (msg[0], msg[1])
        else:
            assert self.devs[board].ctrl_transfer(UM_REQUEST_TYPE, UM_REQUEST, PACLED_VALUE, PACLED_INDEX, msg) == PACLED_MESG_LENGTH

# End class PacLED

# Utility functions:

def mapLogicalIdToBoardAndLED(logicalId):
    '''
    Maps a logical ID in the range of 1 to 256 to a board ID (1-4)
    and a LED number (1-64)
    Returns a tuple (boardId, LED)
    '''
    boardId = ((logicalId-1) / PACLED_LEDS) + 1
    LED  = ((logicalId-1) % PACLED_LEDS) + 1
    return (boardId, LED)

def mapLabelToBoardAndLED(label):
    '''
    Map a text label for a LED to the board and LED number that is wired to that LED
    Returns a tuple (boardId, LED)
    '''
    labelMap = {
            'sw1': (1,1),
            'sw2': (1,2),
            'sw3': (1,3),
            'sw4': (1,4),
            'sw5': (1,5),
            'sw6': (1,6),
            'sw7': (1,7),
            'sw8': (1,8),
            'sw9': (1,9),
            'sw10': (1,10),
            'sw11': (1,11),
            'sw12': (1,12),
            'sw13': (1,13),
            'sw14': (1,14),
            'sw15': (1,15),
            'sw16': (1,16),
            'sw17': (1,17),
            'sw18': (1,18),
            'sw19': (1,19),
            'sw20': (1,20),
            'sw21': (1,21),
            'sw22': (1,22),
            'sw23': (1,23),
            'sw24': (1,24),
            'sw25': (1,25),
            'sw26': (1,26),
            'sw27': (1,27),
            'sw28': (1,28),
            'sw29': (1,29),
            'sw30': (1,30),
            'sw31': (1,31),
            'sw32': (1,32),
            'sw33': (1,33),
            'sw34': (1,34),
            'sw35': (1,35),
            'sw36': (1,36),
            'sw37': (1,37),
            'sw38': (1,38),
            'sw39': (1,39),
            'sw40': (1,40),
            'sw41': (1,41),
            'sw42': (1,42),
            'sw43': (1,43),
            'sw44': (1,44),
            'sw45': (1,45),
            'sw46': (1,46),
            'sw47': (1,47),
            'sw48': (1,48),
            'sw49': (1,49),
            'sw50': (1,50),
            'sw51': (1,51),
            'sw52': (1,52),
            'sw53': (1,53),
            'sw54': (1,54),
            'sw55': (1,55),
            'sw56': (1,56),
            'sw57': (1,57),
            'sw58': (1,58),
            'sw59': (1,59),
            'sw60': (1,60),
            'sw61': (1,61),
            'sw62': (1,62),
            'sw63': (1,63),
            'sw64': (1,64)
            }
    return labelMap[label]


#############
# unittests #
#############
class TestController(unittest.TestCase):
    def setUp(self):
        self.dryRun = False

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
        (boardId, LED) = mapLabelToBoardAndLED('sw1')
        print '%s\t%d\t%d' % ('sw1', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('sw2')
        print '%s\t%d\t%d' % ('sw2', boardId, LED)
        (boardId, LED) = mapLabelToBoardAndLED('sw64')
        print '%s\t%d\t%d' % ('sw64', boardId, LED)
        self.assertEqual(boardId, 1, 'Unexpected boardId value')
        self.assertEqual(LED, 64, 'Unexpected boardId value')

    def test_initializeAllPacDrives(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        self.assertEqual(len(pl.devs), MAX_BOARDS, 'Wrong number of PacLEDs found')

        # TODO: Do I need to do this anywhere?
        # for dev in pl.devs:
        #    usb.util.dispose_resources(dev)

    def test_setLEDIntensityPhysicalRamp(self):
        '''
        Set each of 64 LEDs on board 1 to an intensity proportial to the LED number
        '''
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        for LED in range(1, 65):
            pl.setLEDIntensityPhysical(1, LED, LED*4 - 1)
        print 'Visually verify that LED intensity ramps from LED 1 as dimmest to LED 64 as brightest'
        self.assertTrue(True, 'Should never fail')

    def test_setLEDIntensityPhysicalAll(self):
        '''
        Set all LEDs on board 1 maximum intensity
        '''
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.setLEDIntensityPhysical(1, 'ALL', 255)
        print 'Visually verify that all LEDs are at max intensity'
        self.assertTrue(True, 'Should never fail')

    '''
    def test_updateLEDClear(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updateLED(1, 1, True)
        state = pl.getState()
        self.assertEqual(state[1][0], 0x01, 'LED clear prep of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'LED clear prep of MSB wrong')
        pl.updateLED(1, 1, False)
        state = pl.getState()
        self.assertEqual(state[1][0], 0x00, 'LED clear of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'LED clear MSB wrong')

    def test_updatePattern(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updatePattern('ODD_ONLY')
        state = pl.getState()
        # TODO fix next 2 lines
        self.assertEqual(state[1][0], 0x55, 'Pattern update wrong')
        self.assertEqual(state[1][1], 0x55, 'Pattern update wrong')

    def test_updateAllPacLEDs(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updateAllPacLEDs()
        self.assertTrue(True, 'Visually inspect output to see that all board were updated')

    def test_updatePacLED(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updateLED(1, 8, True)
        pl.updatePacLED(1)
        self.assertTrue(True, 'Visually inspect output to see that the board was updated')

'''
# KLRKLR


########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACLED:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    unittest.main()

# TODO:
# Create utility to set a pattern, delay and then set another pattern until list of patterns is complete
# and then start over or end.
