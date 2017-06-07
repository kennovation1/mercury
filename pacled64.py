'''
TODO: Still needs porting to pacled64 from old pac16 design...

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
Function                            low byte            high byte
--------                            --------            ---------
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
PACLED_PINS = 64
MAX_BOARDS = 1

'''
Class represents a set of PacLED boards and pins.
Boards are numbered starting at 1.

General approach is to write state changes to an array of boards where the
value for each is a bitmap for the pins on that board. Then send the state to
the board.
'''
class PacLED:
    def __init__(self, dryRun=True):
        self.dryRun = dryRun
        self.state = []
        for i in range(MAX_BOARDS+1):
            self.state.append([0, 0]) # LSB, MSB. N.B. state[0] is unused.

    def getState(self):
        return self.state

    def getLedState(self, board, pin):
        lowByte  = self.state[board][0]
        highByte = self.state[board][1]

        (lowByteMask, highByteMask) = mapPin(pin)
        return lowByte & lowByteMask or highByte & highByteMask

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

    def updatePin(self, board, pin, state):
        ''' Set a single pin on or off '''
        # TODO: This is still assuming 16-bit pacdrive boards
        (lowByte, highByte) = mapPin(pin)
        if state:
            self.state[board][0] |= lowByte 
            self.state[board][1] |= highByte
        else:
            self.state[board][0] &= ~lowByte & 0xff
            self.state[board][1] &= ~highByte & 0xff
        self.updatePacLED(board)

    def updatePattern(self, pattern):
        ''' Set the output state according to a pattern command '''
        # TODO: This is still assuming 16-bit pacdrive boards
        if pattern == 'ALL_ON':
            value = 0xff
        elif pattern == 'EVEN_ONLY':
            value = 0xaa
        elif pattern == 'ODD_ONLY':
            value = 0x55
        else: # 'ALL_OFF'
            value = 0x00

        for i in range(len(self.state)):
            self.state[i][0] = value
            self.state[i][1] = value

        self.updateAllPacLEDs()

    def updateAllPacLEDs(self):
        ''' Send update to all attached hardware '''
        for board in self.devs:
            self.updatePacLED(board)

    def updatePacLED(self, board):
        ''' Send a command to update the output state of an attached PacLED '''
        # TODO: This is still assuming 16-bit pacdrive boards
        msg = [0x00, 0x00, 0x00, 0x00]
        msg[3] = self.state[board][0] # LSB
        msg[2] = self.state[board][1] # MSB
        if self.dryRun:
            print 'dryRun: 0x%02x 0x%02x' % (msg[2], msg[3])
        else:
            assert self.devs[board].ctrl_transfer(UM_REQUEST_TYPE, UM_REQUEST, PACLED_VALUE, PACLED_INDEX, msg) == PACLED_MESG_LENGTH

# End class PacLED

# Utility functions:

def mapPin(pin):
    '''
    Set bit to enable provided pin. Pin should be in the range 1-16.
    Returns a tuple (highByte, lowByte)
    '''
    # TODO: This is still assuming 16-bit pacdrive boards
    if pin <= 8:
        lowByte = 0x1 << pin-1
        highByte = 0x0
    else:
        lowByte = 0x0
        highByte = 0x1 << pin-9

    return (lowByte, highByte)

def mapLogicalIdToBoardAndPin(logicalId):
    '''
    Maps a logical ID in the range of 1 to 256 to a board ID (1-4)
    and a pin number (1-64)
    Returns a tuple (boardId, pin)
    '''
    boardId = ((logicalId-1) / PACLED_PINS) + 1
    pin  = ((logicalId-1) % PACLED_PINS) + 1
    return (boardId, pin)

def mapLabelToBoardAndPin(label):
    '''
    Map a text label for a LED to the board and pin that the is wired to that LED
    Returns a tuple (boardId, pin)
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

    # TODO @unittest.skip('Only run this if I change mapPin')
    def test_mapPin(self):
        print '\nTest of mapPin'
        for pin in range(1,65):
            (lowByte, highByte) = mapPin(pin)
            print '%d\t0x%02x\t0x%02x' % (pin, highByte, lowByte)
        # A few tests, but mostly just need to read the output when changing the code
        self.assertEqual(pin, 64, 'Unexpected pin value')
        # TODO Fix the next two lines...
        self.assertEqual(highByte, 0x80, 'Unexpected highByte value')
        self.assertEqual(lowByte, 0x0, 'Unexpected lowByte value')

    # TODO @unittest.skip('Only run this if I change mapLogicalIdToBoardAndPin')
    def test_mapLogicalIdToBoardAndPin(self):
        print '\nTest of mapLogicalIdToBoardAndPin'
        # A few tests, but mostly just need to read the output when changing the code
        for logicalId in range(1,65):
            (boardId, pin) = mapLogicalIdToBoardAndPin(logicalId)
            print '%d\t%d\t%d' % (logicalId, boardId, pin)
        self.assertEqual(logicalId, 64, 'Unexpected logicalId value')
        self.assertEqual(boardId, 1, 'Unexpected boardId value')
        self.assertEqual(pin, 64, 'Unexpected pin value')

    # TODO @unittest.skip('Only run this if I change mapLabelToBoardAndPin')
    def test_mapLabelToBoardAndPin(self):
        # A few tests, but mostly just need to read the output when changing the code
        print '\nTest of mapLabelToBoardAndPin'
        (boardId, pin) = mapLabelToBoardAndPin('sw1')
        print '%s\t%d\t%d' % ('sw1', boardId, pin)
        (boardId, pin) = mapLabelToBoardAndPin('sw2')
        print '%s\t%d\t%d' % ('sw2', boardId, pin)
        self.assertEqual(boardId, 1, 'Unexpected boardId value')
        self.assertEqual(pin, 2, 'Unexpected boardId value')

    def test_initializeAllPacDrives(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        self.assertEqual(len(pl.devs), MAX_BOARDS, 'Wrong number of PacLEDs found')

        # TODO: Do I need to do this anywhere?
        # for dev in pl.devs:
        #    usb.util.dispose_resources(dev)

    def test_getState(self):
        pl = PacLED(dryRun=self.dryRun)
        state = pl.getState()
        print 'getState returned:'
        print state
        self.assertEqual(len(state), MAX_BOARDS+1, 'Wrong length for state')

    def test_updatePinSet(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updatePin(1, 64, True)
        state = pl.getState()
        # TODO fix the next 2 lines
        self.assertEqual(state[1][0], 0x00, 'Pin update of LSB wrong')
        self.assertEqual(state[1][1], 0x80, 'Pin update of MSB wrong')

    def test_updatePinClear(self):
        pl = PacLED(dryRun=self.dryRun)
        pl.initializeAllPacLEDs()
        pl.updatePin(1, 1, True)
        state = pl.getState()
        self.assertEqual(state[1][0], 0x01, 'Pin clear prep of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'Pin clear prep of MSB wrong')
        pl.updatePin(1, 1, False)
        state = pl.getState()
        self.assertEqual(state[1][0], 0x00, 'Pin clear of LSB wrong')
        self.assertEqual(state[1][1], 0x00, 'Pin clear MSB wrong')

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
        pl.updatePin(1, 8, True)
        pl.updatePacLED(1)
        self.assertTrue(True, 'Visually inspect output to see that the board was updated')


########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    unittest.main()

# TODO:
# Create utility to set a pattern, delay and then set another pattern until list of patterns is complete
# and then start over or end.
