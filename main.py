from fastapi import (
    FastAPI, WebSocket, WebSocketDisconnect, Request
)
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Locate templates provided by Jinja2Templates
templates = Jinja2Templates(directory="templates")


# Root api endpoint
@app.get("/")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Subsribe on broadcast of Chat
@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
        count = 0
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                if (data):
                    count += 1
                    data.update({"count": count})
                    await websocket.send_json(data)
        except WebSocketDisconnect:
            websocket.close()