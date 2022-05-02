-- https://www.postgresql.org/docs/14/runtime-config-statistics.html#RUNTIME-CONFIG-STATISTICS-MONITOR

SET log_statement_stats = on;
-- SET log_parser_stats = on;
-- SET log_planner_stats = on;
-- SET log_executor_stats = on;
\ir default.sql
SET log_statement_stats = off;
-- SET log_parser_stats = off;
-- SET log_planner_stats = off;
-- SET log_executor_stats = off;