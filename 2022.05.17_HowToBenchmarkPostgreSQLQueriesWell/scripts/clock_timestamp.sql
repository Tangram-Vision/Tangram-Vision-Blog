-- https://stackoverflow.com/a/9064100

\ir clock_timestamp_function.sql

SELECT * FROM bench('SELECT * FROM artists');
