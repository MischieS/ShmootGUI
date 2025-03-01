import redis
import json

# Initialize Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 📌 Function: Store Real-Time Market Data in Redis
def store_market_data(symbol, price_data):
    redis_client.set(f"trade:{symbol}_1m", json.dumps(price_data))
    redis_client.publish(f"trade_updates:{symbol}", json.dumps(price_data))
    print(f"Updated Redis: {price_data}")

# 📌 Function: Fetch Market Data from Redis
def get_market_data(symbol):
    data = redis_client.get(f"trade:{symbol}_1m")
    return json.loads(data) if data else None
