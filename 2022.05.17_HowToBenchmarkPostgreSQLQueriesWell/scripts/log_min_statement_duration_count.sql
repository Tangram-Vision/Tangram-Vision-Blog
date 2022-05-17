-- https://www.postgresql.org/docs/9.1/runtime-config-logging.html#GUC-LOG-MIN-DURATION-STATEMENT

SET log_min_duration_statement = 0;
\ir default_count.sql
SET log_min_duration_statement = -1;