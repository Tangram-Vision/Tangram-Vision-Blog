# Generating Test Data for PostgreSQL

## Purpose

Demonstrate several different approaches to generating test data in a
PostgreSQL database.

## Blog post

- 2021.04.30: [Creating PostgreSQL Test Data with SQL, PL/pgSQL and Python](https://www.tangramvision.com/blog/creating-postgresql-test-data-with-sql-pl-pgsql-and-python)

## Usage

This project uses Docker to run the PostgreSQL database, to avoid installing
a bunch of packages on your machine and potentially running into different
platform and environment issues.

If you don't have Docker, please visit https://docs.docker.com/get-docker/.

First, use the Dockerfile to build a Docker image:

```
docker build . --tag=postgres-test-data-blogpost
```

Run the Docker image to start a PostgreSQL database:

```
docker run --name=postgres --rm --env=POSTGRES_PASSWORD=foo \
    --volume=$(pwd)/schema.sql:/docker-entrypoint-initdb.d/schema.sql \
    --volume=$(pwd):/repo \
    postgres-test-data-blogpost -c log_statement=all
```

With a postgres container running, you can then run an SQL script that adds
data (these scripts are prefixed with `add-data-`) with:

```
docker exec --workdir=/repo postgres \
    psql --host=localhost --username=postgres \
         --file=add-data-insert-random.sql
```

To poke around the database interactively in psql:

```
docker exec --interactive --tty postgres \
    psql --host=localhost --username=postgres
```

An example query for showing all data:

```
SELECT * FROM artists
    LEFT OUTER JOIN albums USING (artist_id)
    LEFT OUTER JOIN album_genres USING (album_id)
    LEFT OUTER JOIN genres USING (genre_id);
```

If you edit `schema.sql`, you'll need to restart the postgres database
container.  If you edit any of the SQL files, changes will be immediately
reflected inside the container where this folder is mounted at `/repo`.  So,
you can just run the `docker exec` command and your edits will take effect.

NOTE: These scripts have been tested against PostgreSQL versions 12 and 13,
but they likely work in other versions and in databases other than PostgreSQL
as well.