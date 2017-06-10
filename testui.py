'''
File: testui.py

Quick and dirty utility to help debug wiring.

Author: Ken Robbins

'''
import pacled64
import logging
import time
import random

Intensity = 255
BoardList = [1]


def printHelp():
    print '''
      Commands:
        q               Quit
        on <pinlist>       Turn on all pins in the comma separated list (no spaces). All on if no args.
        intensity <value>  Set the default 'on' intensity (1-255)
        board <board>      Set active board (for 'on' command)
        off <pinlist>      Turn of pins in list. All off if no args.
        even               Turn on even pins
        odd                Turn on odd pins
        chase <boardlist>  Rotate lamps in the specified boards in board list order. 1,2,3,4 if no args.
        rand <boardlist>   Random pattern in the specified boards in board. All boards if no args.
    '''

def processUserInput():
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
        elif command == 'even':
            pl.setLEDPattern('EVEN_ON', Intensity, board=board)
        elif command == 'odd':
            pl.setLEDPattern('ODD_ON', Intensity, board=board)
        elif command == 'chase':
            handleChase(args)
        elif command == 'rand':
            handleRandom(args)
        elif command == 'board' or command == 'b':
            board = int(args[0])
            print 'Active board now: ' + str(board)
        else:
            print 'Unknown command'
            printHelp()

def handleOnOffCommand(board, args, state):
    if args and len(args) > 0:
        for pin in args:
            pl.setLEDIntensity(int(pin), Intensity, board=1)
    else:
        if state:
            pl.setLEDPattern('ALL_ON', Intensity, board=1)
        else:
            pl.setLEDPattern('ALL_OFF', Intensity, board=1)

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
    pl.setLEDPattern('ALL_OFF', Intensity, board=board)
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
            for pin in range(0, 64):
                pl.setLEDIntensity(lastPin, 0, board=lastBoard)
                pl.setLEDIntensity(pin, Intensity, board=board)
                lastBoard = board
                lastPin = pin
                time.sleep(0.25)
    pl.setLEDIntensity(lastPin, 0, board=lastBoard)
    pl.setLEDPattern('ALL_OFF', Intensity, board=board)
    print 'Chase done'

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


