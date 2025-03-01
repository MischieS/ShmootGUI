import pandas as pd
import json
import redis
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# Load Config
with open("strategy/strategy_config.json", "r") as f:
    config = json.load(f)

FEATURE_SETTINGS = config["features"]

# Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 📌 Function: Run Traditional Indicator-Based Strategy
def run_traditional_strategy(live_data):
    df = pd.DataFrame([live_data])  # Convert live data to DataFrame
    
    # Compute Indicators
    for period in FEATURE_SETTINGS["ema_periods"]:
        df[f"ema_{period}"] = EMAIndicator(df["close"], window=period).ema_indicator()

    df["rsi"] = RSIIndicator(df["close"], window=FEATURE_SETTINGS["rsi_period"]).rsi()

    # 📌 Example Strategy: EMA Crossover + RSI Confirmation
    if df["ema_5"].iloc[-1] > df["ema_10"].iloc[-1] and df["rsi"].iloc[-1] < 70:
        return "BUY"
    elif df["ema_5"].iloc[-1] < df["ema_10"].iloc[-1] and df["rsi"].iloc[-1] > 30:
        return "SELL"
    
    return None
