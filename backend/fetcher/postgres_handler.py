import psycopg2

# PostgreSQL Connection
def get_db_connection():
    return psycopg2.connect(
        dbname="trading_bot",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )

# 📌 Function: Fetch Historical Market Data
def fetch_historical_data(symbol):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM market_data_{symbol}_1m ORDER BY timestamp DESC LIMIT 100;")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

# 📌 Function: Insert New Market Data (Ensuring No Duplicates)
def insert_historical_data(symbol, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for candle in data:
        timestamp, open_price, high_price, low_price, close_price, volume = candle
        cursor.execute(f"""
            INSERT INTO market_data_{symbol}_1m (timestamp, open_price, high_price, low_price, close_price, volume)
            VALUES (TO_TIMESTAMP({timestamp}/1000), {open_price}, {high_price}, {low_price}, {close_price}, {volume})
            ON CONFLICT (timestamp) DO NOTHING;
        """)

    conn.commit()
    cursor.close()
    conn.close()
