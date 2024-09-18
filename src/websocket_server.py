import asyncio
import websockets
from config import WEBSOCKET_PORT

class WebSocketServer:
    def __init__(self):
        self.clients = set()

    async def start_server(self):
        async with websockets.serve(self.handler, "localhost", WEBSOCKET_PORT):
            await asyncio.Future()  # Run loop forever

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                pass  # when no incoming messages expected
        finally:
            self.clients.remove(websocket)

    async def send_data(self, data):
        if data is None:
            return
        if self.clients:
            await asyncio.wait([client.send(data) for client in self.clients])
