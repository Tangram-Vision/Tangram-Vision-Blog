# Hands-on with PostgreSQL Authorization (Part 1): Roles and Grants

## Purpose

Explain the why and how of using PostgreSQL authorization, specifically roles
and grants (with row-level security policies to come in a future blogpost).

## Blog post

- 2021.12.13: [Hands-on with PostgreSQL Authorization (Part 1): Roles and Grants](https://www.tangramvision.com/blog/hands-on-with-postgresql-authorization-part-1-roles-and-grants)

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
