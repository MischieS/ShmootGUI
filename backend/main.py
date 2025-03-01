from fastapi import FastAPI
import asyncio
from api.endpoints import router as rest_router
from api.websockets import start_websocket_server

app = FastAPI()

# Include REST API routes
app.include_router(rest_router)

@app.on_event("startup")
async def startup_event():
    """
    Start the WebSocket server when FastAPI starts.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(start_websocket_server())

@app.get("/")
def root():
    return {"message": "🚀 Backend API is running!"}
