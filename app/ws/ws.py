from fastapi import APIRouter, WebSocket
from typing import Dict
import logging

logger = logging.Logger(__name__)

ws_router = APIRouter()

USERS: Dict[str, WebSocket] = {}


@ws_router.get("/qwe")
def index() -> Dict[str, str]:
    logger.error(USERS)
    return {"message": "Hello, world!"}


# пример чата на вебсокете между двумя пользователями
@ws_router.websocket('/ws')
async def ws(websocket: WebSocket):
    await websocket.accept()
    name = await websocket.receive_text()
    USERS[name] = websocket
    while True:
        data = await websocket.receive_text()
        logger.error(data)
        if USERS['111'] == websocket:
            await USERS['222'].send_text(data)
        else:
            await USERS['111'].send_text(data)
