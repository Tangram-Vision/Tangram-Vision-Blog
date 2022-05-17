-- https://www.postgresql.org/docs/current/pgbench.html

\! pgbench -f scripts/pg_bench_count_script.sql --log -t 100 --username=postgres postgres