-- https://www.postgresql.org/docs/current/pgstatstatements.html

-- NOTE: The database must be started with the config:
--       shared_preload_libraries='pg_stat_statements'
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

\o /dev/null
-- Warm the cache
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;

-- Reset the stats
SELECT pg_stat_statements_reset();

SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
SELECT * FROM artists;
\o

SELECT * FROM pg_stat_statements WHERE query = 'SELECT * FROM artists';