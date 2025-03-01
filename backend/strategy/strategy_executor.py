import json
import redis
from strategy.ml.model_handler import predict_trade_signal
from strategy.strategy_loader import run_traditional_strategy
from trade.trade_executor import execute_trade

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Load strategy configuration
with open("strategy/strategy_config.json", "r") as f:
    config = json.load(f)

STRATEGY_TYPE = config.get("strategy_type", "ml")  # "ml" or "traditional"

# 📌 Function: Run Selected Strategy
def run_strategy():
    symbol = "BTCUSDT_1m"
    live_data = redis_client.get(f"trade:{symbol}")
    if not live_data:
        return
    
    live_data = json.loads(live_data)

    if STRATEGY_TYPE == "ml":
        signal = predict_trade_signal(live_data)
    else:
        signal = run_traditional_strategy(live_data)

    if signal:
        execute_trade(signal)
