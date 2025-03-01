import ccxt
import psycopg2
import redis
import json
import asyncio

# Initialize Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# PostgreSQL Connection
def get_db_connection():
    return psycopg2.connect(
        dbname="trading_bot",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )

# Binance API
exchange = ccxt.binance()

# 📌 Function: Fetch Historical OHLCV Data & Store in PostgreSQL
def fetch_historical_data(symbol="BTC/USDT", timeframe="1m", limit=1000):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS market_data_BTCUSDT_1m (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            open_price FLOAT NOT NULL,
            high_price FLOAT NOT NULL,
            low_price FLOAT NOT NULL,
            close_price FLOAT NOT NULL,
            volume FLOAT NOT NULL
        );
    """)

    for candle in ohlcv:
        timestamp, open_price, high_price, low_price, close_price, volume = candle
        cursor.execute(f"""
            INSERT INTO market_data_BTCUSDT_1m (timestamp, open_price, high_price, low_price, close_price, volume)
            VALUES (TO_TIMESTAMP({timestamp}/1000), {open_price}, {high_price}, {low_price}, {close_price}, {volume})
            ON CONFLICT (timestamp) DO NOTHING;
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Historical data stored successfully.")

# 📌 Function: Fetch Live Price & Store in Redis
async def fetch_live_price(symbol="BTC/USDT"):
    while True:
        ticker = exchange.fetch_ticker(symbol)
        live_data = {
            "timestamp": ticker["timestamp"],
            "open": ticker["open"],
            "high": ticker["high"],
            "low": ticker["low"],
            "close": ticker["close"],
            "volume": ticker["baseVolume"]
        }

        redis_client.set("trade:BTCUSDT_1m", json.dumps(live_data))
        redis_client.publish("trade_updates:BTCUSDT_1m", json.dumps(live_data))

        print(f"Updated Redis: {live_data}")

        await asyncio.sleep(1)  # Fetch data every second

# Run Data Fetching Tasks
if __name__ == "__main__":
    fetch_historical_data()
    asyncio.run(fetch_live_price())
