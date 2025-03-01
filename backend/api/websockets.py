import json
import asyncio
import websockets
from fetcher.redis_handler import fetch_live_data

async def live_data_handler(websocket, path):
    """
    WebSocket handler for live market data.
    """
    try:
        while True:
            # Example: Get BTC/USDT 1m data from Redis
            live_data = fetch_live_data("BTCUSDT", "1m")
            if live_data:
                await websocket.send(json.dumps(live_data))
            await asyncio.sleep(1)  # Update every second
    except websockets.exceptions.ConnectionClosed:
        print("🔌 WebSocket client disconnected.")

# Start WebSocket server
async def start_websocket_server():
    async with websockets.serve(live_data_handler, "0.0.0.0", 8765):
        print("✅ WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # Keep running
