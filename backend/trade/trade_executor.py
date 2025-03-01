import ccxt
import json
import logging

# Configure logging
logging.basicConfig(filename="trade/trade_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Load API Keys (From .env or config)
with open(".env", "r") as f:
    api_keys = json.load(f)

# Initialize Binance Exchange
exchange = ccxt.binance({
    "apiKey": api_keys["BINANCE_API_KEY"],
    "secret": api_keys["BINANCE_SECRET_KEY"],
    "options": {"defaultType": "spot"},
    "enableRateLimit": True
})

# Load Risk Management Settings
with open("strategy/strategy_config.json", "r") as f:
    config = json.load(f)
RISK_SETTINGS = config["risk_management"]

# 📌 Function: Place Market Order
def execute_trade(signal, symbol="BTC/USDT", amount=0.001):
    try:
        if signal == "BUY":
            order = exchange.create_market_buy_order(symbol, amount)
        elif signal == "SELL":
            order = exchange.create_market_sell_order(symbol, amount)
        else:
            return
        
        # Log trade
        logging.info(f"Executed {signal} Order: {order}")
        print(f"Trade Executed: {signal} {amount} {symbol}")
        
        # Apply Stop-Loss & Take-Profit
        apply_risk_management(signal, symbol)

    except Exception as e:
        logging.error(f"Trade Execution Error: {e}")
        print(f"Trade Execution Failed: {e}")

# 📌 Function: Apply Risk Management (Stop-Loss & Take-Profit)
def apply_risk_management(signal, symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        last_price = ticker["last"]
        
        stop_loss = last_price * (1 - RISK_SETTINGS["stop_loss"]) if signal == "BUY" else last_price * (1 + RISK_SETTINGS["stop_loss"])
        take_profit = last_price * (1 + RISK_SETTINGS["take_profit"]) if signal == "BUY" else last_price * (1 - RISK_SETTINGS["take_profit"])

        # Place Stop-Loss Order
        exchange.create_order(symbol, "stop_market", "sell" if signal == "BUY" else "buy", 0.001, stop_loss, {"stopPrice": stop_loss})
        
        # Place Take-Profit Order
        exchange.create_order(symbol, "take_profit_market", "sell" if signal == "BUY" else "buy", 0.001, take_profit, {"stopPrice": take_profit})
        
        print(f"Stop-Loss at {stop_loss}, Take-Profit at {take_profit}")

    except Exception as e:
        logging.error(f"Risk Management Error: {e}")
        print(f"Risk Management Failed: {e}")
