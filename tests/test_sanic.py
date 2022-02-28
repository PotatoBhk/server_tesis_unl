from sanic import Sanic
from tests.client_manager_sanic import ClientManager
import asyncio
import time

app = Sanic(__name__)

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_MAX_QUEUE = 32
app.config.WEBSOCKET_READ_LIMIT = 2 ** 16
app.config.WEBSOCKET_WRITE_LIMIT = 2 ** 16
app.config.WEBSOCKET_PING_INTERVAL = 100
app.config.WEBSOCKET_PING_TIMEOUT = None

client_manager_vs = ClientManager()
print("efe")

@app.websocket("/state")
async def feed(request, ws):
    print("Started Connection | Process: STATE DETECTIONS |...")
    while True:
        recv = asyncio.create_task(ws.recv())
        json_data = await recv
        await asyncio.wait({asyncio.create_task(ws.send(json_data))})
        
@app.websocket("/stream")
async def stream(request, ws):
    print("Started Connection | Process: VIDEO STREAMING |...")
    init = 0
    await client_manager_vs._subscribe(ws)
    print(client_manager_vs.__len__())
    while True:
        init = init + 1
        recv = asyncio.create_task(ws.recv())
        bytestream = await recv    
        start_time = time.time()
        await client_manager_vs._broadcast(bytestream)
        print("Tiempo estimado: ", time.time() - start_time)
        print("Sent bytestream - Init: ", init)
        
@app.websocket("/register_vs")
async def register_vs(request, ws):
    print("Started Connection | Process: VIDEO STREAMING |...")
    await client_manager_vs._subscribe(ws)
    await ws.recv()

if __name__ == '__main__':
    app.run(port=5000)