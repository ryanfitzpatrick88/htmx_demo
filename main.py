from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse

from app.core.event_bus import ConnectionManager
from app.core.unauthorized_exception import UnauthenticatedAccessException


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Import routers
from app.api.routes import router as api_router

app.include_router(api_router)

@app.exception_handler(UnauthenticatedAccessException)
async def unauthenticated_access_exception_handler(request: Request, exc: UnauthenticatedAccessException):
    return RedirectResponse(url='/auth/login')

manager = ConnectionManager()
app.state.connection_manager = manager

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await app.state.connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await app.state.connection_manager.broadcast(data)
    except WebSocketDisconnect:
        app.state.connection_manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

