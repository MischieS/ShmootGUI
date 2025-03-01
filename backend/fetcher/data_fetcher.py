import ccxt
import datetime
import json
import time
import redis
import threading
import psycopg2
from fetcher.postgres_handler import insert_market_data
from fetcher.redis_handler import store_live_data

exchange = ccxt.binance()

# Redis connection
redis_client = redis.Redis(host="redis", port=6379, db=0)

def fetch_historical_data(symbol, timeframe, limit=1000):
    """
    Fetches historical market data from Binance and stores it in PostgreSQL.
    """
    print(f"📊 Fetching historical data for {symbol} {timeframe} (Limit: {limit})...")

    timeframe_mapping = {
        "1m": "1m", "5m": "5m", "15m": "15m",
        "1h": "1h", "4h": "4h", "1d": "1d"
    }
    
    if timeframe not in timeframe_mapping:
        raise ValueError("Unsupported timeframe!")

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe_mapping[timeframe], limit=limit)
    
    data = [
        (
            datetime.datetime.utcfromtimestamp(candle[0] / 1000),
            candle[1], candle[2], candle[3], candle[4], candle[5]
        ) for candle in ohlcv
    ]
    
    insert_market_data(symbol, timeframe, data)
    print(f"✅ {len(data)} records stored for {symbol} {timeframe}.")
    
    return data

def fetch_live_data(symbol, timeframe):
    """
    Fetches real-time market data from Binance WebSocket and stores it in Redis.
    """
    print(f"📡 Subscribing to WebSocket for {symbol} {timeframe}...")

    def on_message(ws, message):
        data = json.loads(message)
        price_data = {
            "timestamp": data['E'],
            "price": float(data['c']),
            "bid": float(data['b']),
            "ask": float(data['a']),
            "volume": float(data['v'])
        }
        store_live_data(symbol, timeframe, price_data)

    from websocket import WebSocketApp
    url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"
    
    ws = WebSocketApp(url, on_message=on_message)
    
    thread = threading.Thread(target=ws.run_forever)
    thread.start()

    print(f"✅ Live WebSocket data for {symbol} {timeframe} started!")

def ask_user_for_data():
    """
    Ask the user whether they want historical or live data.
    """
    while True:
        choice = input("📊 Do you want [1] Historical data or [2] Live data? ")
        
        if choice == "1":
            symbol = input("Enter currency pair (e.g., BTC/USDT): ").strip()
            timeframe = input("Enter timeframe (e.g., 1m, 5m, 1h): ").strip()
            limit = int(input("Enter data limit (e.g., 1000): "))
            fetch_historical_data(symbol, timeframe, limit)
            break
        elif choice == "2":
            symbol = input("Enter currency pair (e.g., BTC/USDT): ").strip()
            timeframe = input("Enter timeframe (e.g., 1m, 5m, 1h): ").strip()
            fetch_live_data(symbol, timeframe)
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    ask_user_for_data()
