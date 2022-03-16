# Hands-on with PostgreSQL Authorization (Part 2): Row-Level Security

## Purpose

Explain the why and how of using Row-Level Security (RLS) in PostgreSQL.

## Blog post

- 2022.03.16: [Hands-on with PostgreSQL Authorization (Part 2): Row-Level Security](https://www.tangramvision.com/blog/hands-on-with-postgresql-authorization-part-2-row-level-security)

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
    postgres:latest -c log_statement=all
```

To open a psql prompt in that container, run the following in another terminal:

```
docker exec --interactive --tty postgres \
    psql --username=postgres
```
