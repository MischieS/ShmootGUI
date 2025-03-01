from fastapi import APIRouter, Depends
import redis
import psycopg2
import json
from pydantic import BaseModel

router = APIRouter()

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="trading_bot",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )

# API Model for Strategy Settings
class StrategySettings(BaseModel):
    ema_periods: list[int]
    rsi_period: int
    macd_fast: int
    macd_slow: int
    macd_signal: int
    stochastic_k: int
    bollinger_period: int

# 📌 Endpoint: Fetch Live Market Data from Redis
@router.get("/market_data/{symbol}")
def get_market_data(symbol: str):
    data = redis_client.get(f"trade:{symbol}_1m")
    return json.loads(data) if data else {"error": "No data available"}

# 📌 Endpoint: Fetch Historical Market Data from PostgreSQL
@router.get("/historical_data/{symbol}")
def get_historical_data(symbol: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM market_data_{symbol}_1m ORDER BY timestamp DESC LIMIT 100;")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 📌 Endpoint: Update Strategy Settings
@router.post("/update-strategy-config")
def update_strategy_config(config: StrategySettings):
    with open("strategy/strategy_config.json", "w") as f:
        json.dump({"features": config.dict()}, f, indent=4)
    return {"message": "Strategy configuration updated!"}
