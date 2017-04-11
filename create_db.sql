CREATE USER vagrant WITH PASSWORD 'password';
CREATE DATABASE picole;
ALTER ROLE vagrant SET client_encoding TO 'utf8';
ALTER ROLE vagrant SET default_transaction_isolation TO 'read committed';
ALTER ROLE vagrant SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE picole TO vagrant;