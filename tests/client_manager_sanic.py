import asyncio
from sanic.exceptions import WebsocketClosed
from websockets.exceptions import ConnectionClosed

class ClientManager():
    
    def __init__(self):
        print("Initializing manager...")
        self.clients = set()
        
    def __len__(self):
        return len(self.clients)
    
    async def _subscribe(self, client):
        print('Subscribed to manager...')
        self.clients.add(client)
    
    async def _broadcast(self, data):
        print('Broadcasting to {} clients...'.format(len(self.clients)))
        clients = self.clients.copy()
        for client in clients:
            try:
                await client.send(data)
            except Exception:
                print('Closing connection...')
                await self._leave(client)
    
    async def _leave(self, client):
        try:
            self.clients.remove(client)
        except ValueError:
            pass