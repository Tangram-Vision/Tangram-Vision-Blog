# How To Benchmark PostgreSQL Queries Well

## Purpose

Explore and discuss different ways to benchmark execution time of PostgreSQL
queries.

## Blog post

- 2022.05.17: [How To Benchmark PostgreSQL Queries Well](https://www.tangramvision.com/blog/how-to-benchmark-postgresql-queries-well)

## Usage

This project uses Docker to run the PostgreSQL database, to avoid installing
a bunch of packages on your machine and potentially running into different
platform and environment issues.

If you don't have Docker, please visit https://docs.docker.com/get-docker/.

To run the database with the example schema:

```
docker run --name=postgres \
    --rm \
    --volume=$(pwd)/schema.sql:/docker-entrypoint-initdb.d/schema.sql \
    --volume=$(pwd):/repo \
    --env=PSQLRC=/repo/.psqlrc \
    --env=POSTGRES_PASSWORD=foo \
    postgres:latest \
    -c shared_preload_libraries='pg_stat_statements' \
    -c pg_stat_statements.track_planning=on
```

To open a psql prompt in that container, run the following in another terminal:

```
docker exec --interactive --tty \
    --user=postgres \
    --workdir=/repo \
    postgres psql --username=postgres
```
