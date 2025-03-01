import redis
import json

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

def store_live_data(symbol, timeframe, price_data, ttl=60):
    """
    Stores real-time market data in Redis with a Time-To-Live (TTL).
    
    Parameters:
        - symbol (str): The trading pair (e.g., "BTCUSDT").
        - timeframe (str): The selected timeframe (e.g., "1m").
        - price_data (dict): Contains price, bid, ask, volume, and timestamp.
        - ttl (int): Time-To-Live in seconds (default: 60 sec).
    """
    key = f"trade:{symbol}_{timeframe}"
    redis_client.setex(key, ttl, json.dumps(price_data))
    print(f"✅ Live data stored: {symbol} {timeframe}")

def fetch_live_data(symbol, timeframe):
    """
    Retrieves real-time market data from Redis.
    
    Returns:
        - dict: Price data if found.
        - None: If no data is available.
    """
    key = f"trade:{symbol}_{timeframe}"
    trade_data = redis_client.get(key)
    
    if trade_data:
        return json.loads(trade_data)
    else:
        print(f"⚠️ No live data found for {symbol} {timeframe}")
        return None
