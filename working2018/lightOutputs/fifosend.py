# Simulate sending commands to light controller
# Test as follows:
# python recv.py &
# python send.py

import json
import os
import errno
from time import sleep

messages = [
            {
            'type': 'PHYSICAL',
            'target': 0,
            'action': 'off'
            },
            {
            'type': 'LOGICAL',
            'target': 'CABIN PRESS',
            'subtarget': 'amber',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'O2 QUAN',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'O2 EMER',
            'subtarget': 'amber',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'EXCESS SUIT H20',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'EXCESS CABIN H20',
            'subtarget': 'amber',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'FUEL QUAN',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO WARN',
            'subtarget': 'left',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO WARN',
            'subtarget': 'right',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO RESET',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'STBY AC-AUTO',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'EXCESS CABIN H20',
            'subtarget': 'amber',
            'action': 'on',
            'intensity': 255
            },
            {
            'type': 'LOGICAL',
            'target': 'all',
            'action': 'off'
            },

            {
            'type': 'LOGICAL',
            'target': 'ABORT',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO SEQ',
            'subtarget': 'left',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO SEQ',
            'subtarget': 'right',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRO ATT',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'FIRE RETRO',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'FIRE RETRO',
            'subtarget': 'red',
            'action': 'off',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'FIRE RETRO',
            'subtarget': 'green',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'JETT RETRO',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RETRACT SCOPE',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': '.05G',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'MAIN',
            'subtarget': 'red',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'LANDING BAG',
            'subtarget': 'left',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RESCUE',
            'subtarget': 'left',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'RESCUE',
            'subtarget': 'right',
            'action': 'on',
            'intensity': 50
            },
            {
            'type': 'LOGICAL',
            'target': 'all',
            'action': 'off'
            },

        ]

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

FIFO = '/tmp/light-commands'

makeFifo(FIFO)

# Open and writes will block if no reader on fifo (or if full)
with open(FIFO, 'w') as fp:
    for message in messages:
        buff = json.dumps(message) + '\n'
        # Newline makes it possible to use readline on the other size so that I have a good message boundary
        fp.write(buff)
        sleep(0.25)
        fp.flush()

