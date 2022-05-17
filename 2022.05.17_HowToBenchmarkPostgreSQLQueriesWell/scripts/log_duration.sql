-- https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-DURATION

SET log_duration = on;
\ir default.sql
SET log_duration = off;