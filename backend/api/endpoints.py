from fastapi import APIRouter
from fetcher.postgres_handler import connect_postgres
from fetcher.redis_handler import fetch_live_data

router = APIRouter()

@router.get("/historical/{symbol}/{timeframe}/{limit}")
def get_historical_data(symbol: str, timeframe: str, limit: int):
    """
    Fetch historical data from PostgreSQL.
    """
    table_name = f"market_data_{symbol.replace('/', '')}_{timeframe}"
    
    query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT {limit}"
    
    conn = connect_postgres()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"symbol": symbol, "timeframe": timeframe, "data": rows}

@router.get("/live/{symbol}/{timeframe}")
def get_live_data(symbol: str, timeframe: str):
    """
    Fetch real-time market data from Redis.
    """
    live_data = fetch_live_data(symbol, timeframe)
    return {"symbol": symbol, "timeframe": timeframe, "data": live_data}
