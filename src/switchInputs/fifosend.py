# Simulate sending events to capsule controller
# Test as follows:
# python recv.py &
# python send.py

import json
import os
import errno

def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise

def makeMessage(count):
    ''' Send a small number of simulated messages '''
    event = {
        'name': 'MESG_' + str(i),
        'type': 'toggleSwitch',
        'description': 'Message ' + str(i)
        }
    return json.dumps(event) + '\n'
    # Newline makes it possible to use readline on the other size so that I have a good message boundary


############
# Main
############

FIFO = '/tmp/mercury-events'

makeFifo(FIFO)

# Open and writes will block if no reader on fifo (or if full)
with open(FIFO, 'w') as fp:
    for i in range(4):
        fp.write(makeMessage(i))
        fp.flush()

