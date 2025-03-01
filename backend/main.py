from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.endpoints import router as api_router
from api.websockets import websocket_router

# Initialize FastAPI App
app = FastAPI(title="Shmoot Scalping Bot API", version="1.0")

# CORS Middleware (Allows Frontend to Access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routes
app.include_router(api_router, prefix="/api")
app.include_router(websocket_router, prefix="/ws")

# Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
