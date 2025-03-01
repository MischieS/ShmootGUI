import psycopg2
import json

# Load Database Config
with open(".env", "r") as f:
    db_config = json.load(f)

# 📌 Function: Get PostgreSQL Connection
def get_db_connection():
    return psycopg2.connect(
        dbname=db_config["DB_NAME"],
        user=db_config["DB_USER"],
        password=db_config["DB_PASSWORD"],
        host=db_config["DB_HOST"],
        port=db_config["DB_PORT"]
    )

# 📌 Function: Fetch Market Data
def fetch_market_data(symbol, limit=100):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM market_data_{symbol}_1m ORDER BY timestamp DESC LIMIT {limit};"
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows
