import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        mesg = await websocket.recv()
        print('Got message: ' + mesg)

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:8765'))
