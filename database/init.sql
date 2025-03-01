-- 📌 Create OHLCV Market Data Table
CREATE TABLE IF NOT EXISTS market_data_BTCUSDT_1m (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP UNIQUE NOT NULL,
    open_price FLOAT NOT NULL,
    high_price FLOAT NOT NULL,
    low_price FLOAT NOT NULL,
    close_price FLOAT NOT NULL,
    volume FLOAT NOT NULL
);

-- 📌 Create Trade Execution Table
CREATE TABLE IF NOT EXISTS executed_trades (
    id SERIAL PRIMARY KEY,
    trade_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symbol VARCHAR(20) NOT NULL,
    trade_type VARCHAR(4) CHECK (trade_type IN ('BUY', 'SELL')),
    entry_price FLOAT NOT NULL,
    exit_price FLOAT,
    profit FLOAT
);

-- 📌 Create Strategy Config Table
CREATE TABLE IF NOT EXISTS strategy_config (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(50) NOT NULL,
    settings JSONB NOT NULL
);
