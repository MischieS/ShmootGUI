import pandas as pd
import json
import psycopg2
from strategy.strategy_loader import run_traditional_strategy
from strategy.ml.model_handler import predict_trade_signal

# Load strategy configuration
with open("strategy/strategy_config.json", "r") as f:
    config = json.load(f)
STRATEGY_TYPE = config["strategy_type"]

# PostgreSQL Connection
def get_db_connection():
    return psycopg2.connect(
        dbname="trading_bot",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )

# 📌 Function: Fetch Historical Data
def fetch_historical_data(symbol="BTCUSDT_1m", limit=500):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM market_data_{symbol} ORDER BY timestamp ASC LIMIT {limit};")
    rows = cursor.fetchall()
    
    conn.close()
    
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    return df

# 📌 Function: Run Backtest
def run_backtest():
    df = fetch_historical_data()
    balance = 1000  # Starting balance (USD)
    position = None  # None, "long", or "short"
    entry_price = 0

    for _, row in df.iterrows():
        if STRATEGY_TYPE == "ml":
            signal = predict_trade_signal(row)
        else:
            signal = run_traditional_strategy(row)

        if signal == "BUY" and position is None:
            position = "long"
            entry_price = row["close"]
            print(f"BUY at {entry_price}")

        elif signal == "SELL" and position == "long":
            profit = row["close"] - entry_price
            balance += profit
            position = None
            print(f"SELL at {row['close']} | Profit: {profit:.2f}")

    print(f"Final Balance: {balance:.2f}")

# Run Backtest
if __name__ == "__main__":
    run_backtest()
