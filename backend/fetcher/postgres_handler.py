import psycopg2

def connect_postgres():
    return psycopg2.connect(
        host="postgres",
        database="trading_bot",
        user="trader",
        password="trading_password"
    )

def create_table_if_not_exists(symbol, timeframe):
    """
    Ensures that the PostgreSQL table exists for storing market data.
    """
    table_name = f"market_data_{symbol.replace('/', '')}_{timeframe}"
    
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        open_price FLOAT NOT NULL,
        high_price FLOAT NOT NULL,
        low_price FLOAT NOT NULL,
        close_price FLOAT NOT NULL,
        volume FLOAT NOT NULL
    );
    """
    
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Table {table_name} is ready.")

def insert_market_data(symbol, timeframe, data):
    """
    Inserts market data into PostgreSQL.
    """
    create_table_if_not_exists(symbol, timeframe)
    table_name = f"market_data_{symbol.replace('/', '')}_{timeframe}"
    
    conn = connect_postgres()
    cursor = conn.cursor()
    
    query = f"""
    INSERT INTO {table_name} (timestamp, open_price, high_price, low_price, close_price, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {len(data)} records into {table_name}.")
