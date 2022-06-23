from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, Request
)
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Locate templates provided by Jinja2Templates
templates = Jinja2Templates(directory="templates")


# Root api breakpoint
@app.get("/")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Manager of connections
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

# Subsribe on broadcast of Chat
@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
        count = 0
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                if (data):
                    count += 1
                    data.update({"count": count})
                    await manager.broadcast(data)
        except WebSocketDisconnect:
            manager.disconnect(websocket)