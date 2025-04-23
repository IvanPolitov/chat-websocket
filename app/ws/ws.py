from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from typing import Dict, Tuple

from fastapi.responses import HTMLResponse


ws_router = APIRouter(prefix='/ws')


class ConnectionManager():
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, ip: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[ip] = websocket
        print(self.active_connections)

    def disconnect(self, ip: str):
        self.active_connections.pop(ip)

    async def broadcast(self, message: str):
        for ip, connection in self.active_connections.items():
            await connection.send_text(message)

manager = ConnectionManager()


@ws_router.get('/')
async def index():
    with open('app/ws/template/index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)


@ws_router.websocket('/ws')
async def ws_endpoint(websocket: WebSocket):
    ip = ':'.join((websocket.client.host, str(websocket.client.port)))
    await manager.connect(ip, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f'{ip}: {data}')
    except WebSocketDisconnect:
        manager.disconnect(ip)
        await manager.broadcast(f"A client has left the chat")
