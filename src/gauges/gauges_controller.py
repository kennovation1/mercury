# Initial test websockets server to demonstrate
# how to send gauge values to a websocket client running
# in a browser.
# Browser should run gauges.html
# Apache is running locally and gauges.html is copied to /var/www/html/
# Therefore to test:
#     python gauges_server.py  # This script
#     Browse to http://192.168.1.12:5100/gauges.html
import asyncio
import random  # Only needed to random testing
import websockets
import json
import os
import errno

FIFO = '/tmp/gauge-commands'


def makeFifo(fifoName):
    ''' Create the fifo if it doesn't already exist '''
    try:
        os.mkfifo(fifoName)
    except OSError as oe: 
        if oe.errno != errno.EEXIST:
            raise


async def doWork(websocket, path):
    print('Starting doWork')
    while True:
        mesg = Fp.readline()
        if len(mesg) == 0:
            continue

        command = json.loads(mesg)
        print(command)

        await websocket.send(json.dumps(command))


########
# Main #
########

makeFifo(FIFO)
#with open('test_commands', 'r') as Fp:
print('Waiting to open FIFO')
with open(FIFO, 'r') as Fp:
    print('FIFO opened')
    start_server = websockets.serve(doWork, "192.168.1.12", 5100)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
