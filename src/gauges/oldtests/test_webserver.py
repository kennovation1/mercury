#!/usr/bin/env python3

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import json

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        value = random.random() * 15
        gauge = {
                'gauge': 'CabinPressure',
                'value': value
                }
        await websocket.send(json.dumps(gauge))
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, "192.168.1.12", 5100)
#start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

