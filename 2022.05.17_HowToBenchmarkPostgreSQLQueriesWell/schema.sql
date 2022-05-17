CREATE TABLE artists (
    -- More about identity column:
    -- https://www.2ndquadrant.com/en/blog/postgresql-10-identity-columns/
    -- https://www.depesz.com/2017/04/10/waiting-for-postgresql-10-identity-columns/
    artist_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

-- Generate benchmark/test data
SELECT 10000000 AS _artist_count \gset

INSERT INTO artists (name)
SELECT substr(md5(random()::text), 1, 12)
FROM generate_series(1, :_artist_count) AS _g;

-- If you copy the table to a CSV file to load faster:
-- \copy artists from '/repo/data.csv' csv;


-- Generate statistics on all tables so the query planner can plan effectively.
--
-- For more about planner stats and decision-making, see
-- https://www.depesz.com/2013/05/30/explaining-the-unexplainable-part-5/
ANALYZE;
