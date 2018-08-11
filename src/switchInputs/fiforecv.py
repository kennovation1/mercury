# Test capsule controller to receive events and then actuate outputs (lights, sounds, displays, etc.)
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


############
# Main
############

FIFO = '/tmp/mercury-events'

makeFifo(FIFO)

# Open will block until there is a writer and a message is written
with open(FIFO, 'r') as fp:
    while True:
        # This does not block. Will return 0 if nothing to read
        mesg = fp.readline()
        if len(mesg) > 0:
            event = json.loads(mesg)
            print(json.dumps(event, indent=4))
        else:
            # Could go off and do other things here...
            pass


