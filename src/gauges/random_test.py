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

async def time(websocket, path):
    while True:
        # Get these values from a named pipe that the controller will write to
        gaugeName = 'CabinPressure'
        gaugeValue = random.random() * 15

        gauge = {
                'gauge': gaugeName,
                'value': gaugeValue
                }
        await websocket.send(json.dumps(gauge))

        # This is just for sending random data. Delete once integrated.
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, "192.168.1.12", 5100)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

