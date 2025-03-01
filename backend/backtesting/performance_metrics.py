import pandas as pd
import numpy as np

# 📌 Function: Calculate Performance Metrics
def calculate_performance(trade_log):
    df = pd.DataFrame(trade_log)

    # Profit & Loss
    df["profit"] = df["exit_price"] - df["entry_price"]
    total_profit = df["profit"].sum()
    
    # Win Rate
    win_rate = (df["profit"] > 0).mean() * 100

    # Maximum Drawdown
    running_balance = 1000 + df["profit"].cumsum()
    peak = running_balance.cummax()
    drawdown = (running_balance - peak) / peak
    max_drawdown = drawdown.min()

    # Sharpe Ratio (Risk-Adjusted Return)
    daily_returns = df["profit"] / 1000  # Normalize
    sharpe_ratio = daily_returns.mean() / daily_returns.std()

    return {
        "Total Profit": total_profit,
        "Win Rate (%)": win_rate,
        "Max Drawdown (%)": max_drawdown * 100,
        "Sharpe Ratio": sharpe_ratio
    }

# 📌 Example Trade Log
trade_log = [
    {"entry_price": 63000, "exit_price": 63200},
    {"entry_price": 63500, "exit_price": 63050},
    {"entry_price": 62800, "exit_price": 63100},
]

# 📌 Run Performance Calculation
metrics = calculate_performance(trade_log)
print(metrics)
