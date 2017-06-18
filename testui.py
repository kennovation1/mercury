'''
File: testui.py

Quick and dirty utility to help debug wiring.

Author: Ken Robbins

'''
import pacled64
import logging
import time
import random
import string

Intensity = 255
BoardList = [1]


def printHelp():
    print '''
      Commands:
        (o) on <pinlist>       Turn on all pins in the comma-separated list (no spaces). All on if no args.
        (f) off <pinlist>      Turn of pins in list. All off if no args.
        even                   Turn on even pins
        odd                    Turn on odd pins

        t <telelight>          Turn on comma-separated list of telelights (no spaces). All on if no args.
        T <telelight>          Turn off comma-separated list of telelights (no spaces). All off if no args.
                               Use 'l' or 'r' suffix for left and right respectively.
                               Telelights are numbered from 1 to N.

        chase <boardlist>       Rotate lamps in the specified boards in board list order. 1,2,3,4 if no args.
        rand <boardlist> NOT WORKING Random full on/off pattern in the specified boards in board. All boards if no args.

        (i) intensity <value>  Set the default 'on' intensity (1-255)
        (r) rate <flash rate>  Set a global flash rate (0:no flash, 1:2secs, 2:1sec, 3:0.5secs)
        (s) speed <ramp speed> Set a global on/off ramp speed in 10s of milliseconds
        (b) board <board>      Set active board (for 'on' and 'telelight' commands)
        special                Custom command
        q                      Quit
    '''

def processUserInput():
    global Intensity

    printHelp()
    board = 1
    while True:
        line = raw_input()
        cleanLine = line.rstrip(' \r\n\t')
        if len(cleanLine) == 0:
            continue

        parts = line.split(None, 2)
        command = parts[0]
        print 'Command: %s' % (command)
        if len(parts) == 2: # Assume a comma-separated list of pins
            args = parts[1].split(',')
        else:
            args = None

        if command == 'q':
            print 'Quitting'
            break
        elif command == 'off' or command == 'f':
            handleOnOffCommand(board, args, False)
        elif command == 'on' or command == 'o':
            handleOnOffCommand(board, args, True)
        elif command == 'intensity' or command == 'i':
            Intensity = int(args[0])
            print 'Intensity now: ' + str(Intensity)
        elif command == 'telelight' or command == 't':
            handleTelelightCommand(board, args, True)
        elif command == 'Telelight' or command == 'T':
            handleTelelightCommand(board, args, False)
        elif command == 'rate' or command == 'r':
            rate = int(args[0])
            print 'Flash rate now: ' + str(rate)
            pl.setLEDFlash('ALL', rate, board=board)
        elif command == 'speed' or command == 's':
            speed = int(args[0])
            print 'Ramp on/off speed now: ' + str(speed)
            pl.setRampSpeed(speed, board=board)
        elif command == 'even':
            pl.setLEDPattern('EVEN_ONLY', Intensity, board=board)
        elif command == 'odd':
            pl.setLEDPattern('ODD_ONLY', Intensity, board=board)
        elif command == 'chase':
            handleChase(args)
        elif command == 'rand':
            handleRandom(args)
        elif command == 'board' or command == 'b':
            board = int(args[0])
            print 'Active board now: ' + str(board)
        elif command == 'special':
            handleSpecial(args)
        else:
            print 'Unknown command'
            printHelp()

def handleOnOffCommand(board, args, state):
    if args and len(args) > 0:
        for pin in args:
            if state:
                pl.setLEDIntensity(int(pin), Intensity, board=1)
            else:
                pl.setLEDIntensity(int(pin), 0, board=1)
    else:
        if state:
            pl.setLEDPattern('ALL_ON', Intensity, board=1)
        else:
            pl.setLEDPattern('ALL_OFF', 0, board=1)

def handleTelelightCommand(board, args, state):
    if args and len(args) > 0:
        for telelight in args:
            pins = mapTelelightToPins(telelight)
            for pin in pins:
                if state:
                    pl.setLEDIntensity(pin, Intensity, board=1)
                else:
                    pl.setLEDIntensity(pin, 0, board=1)
    else:
        if state:
            pl.setLEDPattern('ALL_ON', Intensity, board=1)
        else:
            pl.setLEDPattern('ALL_OFF', 0, board=1)

def mapTelelightToPins(telelight):
    left =   [ 16, 17, 18,  4,  5,  6,  7, 8, 24 ] # As viewed from front, top to bottom, main panel
    right =  [  1,  2,  3, 19, 20, 21, 22, 23, 9 ]

    mode = 'b' # Both
    if string.find(telelight, 'l') >= 0:
        mode = 'l'
    elif string.find(telelight, 'r') >= 0:
        mode = 'r'

    num = int(string.rstrip(telelight, 'lr')) - 1

    pins = []

    if mode in ('b', 'l'):
        pins.append(left[num])

    if mode in ('b', 'r'):
        pins.append(right[num])

    return pins

def handleRandom(args):
    lastPin = 1

    if args and len(args) > 0:
        boards = args
    else:
        boards = BoardList

    for i in range(100):
        state = random.choice([Intensity, Intensity, 0])
        board = int(random.choice(boards))
        pin = random.randint(0, 63)
        pl.setLEDIntensity(pin, Intensity, board=board)
        time.sleep(0.25)
    pl.setLEDPattern('ALL_OFF', 0, board=board)
    print 'Rand done'

def handleChase(args):
    lastBoard = 1
    lastPin = 1

    if args and len(args) > 0:
        boards = args
    else:
        boards = BoardList

    for i in range(2):
        for b in boards:
            board = int(b)
            for pin in range(1, 65):
                pl.setLEDIntensity(lastPin, 0, board=lastBoard)
                pl.setLEDIntensity(pin, Intensity, board=board)
                lastBoard = board
                lastPin = pin
                time.sleep(0.25)
    pl.setLEDIntensity(lastPin, 0, board=lastBoard)
    pl.setLEDPattern('ALL_OFF', 0, board=board)
    print 'Chase done'

def handleSpecial(args):
    print 'Special: Runs forever. Control-C to quit'

    last = 9
    for i in range(10):
        for telelight in range(1, 10):
            handleTelelightCommand(1, [str(last)], 0)
            handleTelelightCommand(1, [str(telelight)], Intensity)
            last = telelight
            time.sleep(0.25)

    while(True):
        state = random.choice([Intensity, Intensity, 0])
        telelight = random.randint(1, 9)
        print telelight, state
        handleTelelightCommand(1, [str(telelight)], state)
        time.sleep(0.25)


########
# MAIN #
########
if __name__ == '__main__':
    logFormat = '%(levelname)s:%(asctime)s:PACDRIVE:%(module)s-%(lineno)d: %(message)s'
    logLevel = logging.INFO
    logging.basicConfig(format=logFormat, level=logLevel)

    pl = pacled64.PacLED(dryRun=False)
    pl.initializeAllPacLEDs()

    processUserInput()


