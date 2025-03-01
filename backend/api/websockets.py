from fastapi import APIRouter, WebSocket
import redis
import json

websocket_router = APIRouter()

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 📌 WebSocket: Stream Live Market Data
@websocket_router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"trade_updates:{symbol}")

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
