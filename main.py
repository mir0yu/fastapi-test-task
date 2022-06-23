from re import T
from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, Request, Response
)
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

# locate templates
templates = Jinja2Templates(directory="templates")



@app.get("/")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})



class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append((websocket))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove((websocket))

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)


manager = SocketManager()


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
        await manager.connect(websocket)
        response = {}
        await manager.broadcast(response)
        try:
            while True:
                data = await websocket.receive_json()
                await manager.broadcast(data)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            response['message'] = "left"
            await manager.broadcast(response)