import joblib
import pandas as pd
import redis
import json

# Load trained XGBoost model
model = joblib.load("strategy/ml/models/xgboost_model.pkl")

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Features used for prediction
features = ["ma_10", "ma_50", "rsi", "macd", "bb_high", "bb_low"]

def fetch_live_data():
    """Fetches real-time data from Redis and formats it for model prediction."""
    raw_data = redis_client.get("trade:BTCUSDT_1m")
    if raw_data:
        market_data = json.loads(raw_data)
        df = pd.DataFrame([market_data])  # Convert to DataFrame
        return df[features]
    return None

def predict_trade_signal():
    """Uses the trained XGBoost model to predict whether to Buy (1) or Sell (0)."""
    live_data = fetch_live_data()
    if live_data is not None:
        prediction = model.predict(live_data)[0]
        action = "BUY" if prediction == 1 else "SELL"
        print(f"Predicted Trade Signal: {action}")
        return action
    return None
