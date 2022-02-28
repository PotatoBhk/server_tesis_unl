import asyncio
import time
import websocket

f = open("sample.jpg", "wb")

ws = websocket.WebSocket()
ws.connect("ws://localhost:5000/register_vs")
img_bytes = ws.recv()
f.write(img_bytes)
f.close()
ws.close()