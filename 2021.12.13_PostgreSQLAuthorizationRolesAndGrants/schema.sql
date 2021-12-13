CREATE TABLE artists (
    -- More about identity column:
    -- https://www.2ndquadrant.com/en/blog/postgresql-10-identity-columns/
    -- https://www.depesz.com/2017/04/10/waiting-for-postgresql-10-identity-columns/
    artist_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE albums (
    album_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    artist_id INTEGER REFERENCES artists(artist_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    released DATE NOT NULL
);

CREATE TABLE fans (
    fan_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

CREATE TABLE fan_follows (
    fan_id INTEGER REFERENCES fans(fan_id) ON DELETE CASCADE,
    artist_id INTEGER REFERENCES artists(artist_id) ON DELETE CASCADE,
    PRIMARY KEY (fan_id, artist_id)
);
