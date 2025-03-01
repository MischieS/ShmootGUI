import ccxt
import json

# Load API Keys
with open(".env", "r") as f:
    api_keys = json.load(f)

# Initialize Binance Exchange
exchange = ccxt.binance({
    "apiKey": api_keys["BINANCE_API_KEY"],
    "secret": api_keys["BINANCE_SECRET_KEY"],
    "options": {"defaultType": "spot"},
    "enableRateLimit": True
})

# Load Risk Settings
with open("strategy/strategy_config.json", "r") as f:
    config = json.load(f)
RISK_SETTINGS = config["risk_management"]

# 📌 Function: Get Available Capital for Trading
def get_available_balance():
    balance = exchange.fetch_balance()
    return balance["free"]["USDT"]

# 📌 Function: Calculate Trade Size Based on Capital
def calculate_trade_size(symbol="BTC/USDT"):
    available_capital = get_available_balance()
    risk_per_trade = available_capital * RISK_SETTINGS["trade_risk_percent"]  # Example: 2% risk per trade
    last_price = exchange.fetch_ticker(symbol)["last"]
    trade_size = risk_per_trade / last_price
    return round(trade_size, 6)

# 📌 Function: Validate Risk Before Placing a Trade
def validate_risk(trade_size):
    if trade_size < 0.0001:  # Minimum trade size on Binance
        print("Trade size too small, skipping trade.")
        return False
    return True
