CREATE DATABASE trading_bot;
CREATE USER trader WITH ENCRYPTED PASSWORD 'trading_password';
GRANT ALL PRIVILEGES ON DATABASE trading_bot TO trader;

-- This script will not create fixed tables, but tables will be created dynamically in Python
