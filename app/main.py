import asyncio
import os
import sys
from fastapi import FastAPI, WebSocket
import uvicorn
import logging
from typing import Dict


proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..'))
if proj_dir not in sys.path:
    sys.path.append(proj_dir)


from db.base import create_db  # noqa
from api.users import user_router  # noqa
from ws.ws import ws_router  # noqa

app = FastAPI()
app.include_router(user_router)
app.include_router(ws_router)


@app.get("/")
def welcome():
    return {'message': 'Welcome'}


if __name__ == '__main__':
    asyncio.run(create_db())
    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
