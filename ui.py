import asyncio
import websockets
import threading
from collections import deque
import time


class UI:
    def __init__(self, event_loop):
        self.server_thread = threading.Thread(target=self.serve)
        self.server_thread.start()
        self.queue = deque()

    def serve(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.handle, "localhost", 8765)
        )
        asyncio.get_event_loop().run_forever()

    def send(self, message):
        self.queue.appendleft(f"{time.time()}:{message}")

    async def handle(self, websocket, path):
        try:
            while True:
                if len(self.queue):
                    message = self.queue.pop()
                    await websocket.send(message)
                else:
                    time.sleep(0.5)
        except websockets.exceptions.ConnectionClosedError:
            print("Client disconnected")
