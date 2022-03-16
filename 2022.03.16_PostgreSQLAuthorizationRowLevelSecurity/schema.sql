CREATE TABLE artists (
    -- More about identity column:
    -- https://www.2ndquadrant.com/en/blog/postgresql-10-identity-columns/
    -- https://www.depesz.com/2017/04/10/waiting-for-postgresql-10-identity-columns/
    artist_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE albums (
    album_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    artist_id INTEGER NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
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

CREATE TABLE songs (
    song_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    album_id INTEGER NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
    title TEXT NOT NULL
);


-- Create roles that will access the database
CREATE ROLE fan LOGIN;
CREATE ROLE artist LOGIN;

-- Grant base privileges, as explored in previous article. See:
-- Code: ../2021.12.13_PostgreSQLAuthorizationRolesAndGrants/tutorial.sql
-- Article: https://www.tangramvision.com/blog/hands-on-with-postgresql-authorization-part-1-roles-and-grants
GRANT SELECT, DELETE ON fans TO fan;
GRANT SELECT, INSERT, DELETE ON fan_follows TO fan;
GRANT SELECT ON artists TO fan;
GRANT SELECT ON albums TO fan;
GRANT SELECT ON songs TO fan;
GRANT SELECT, UPDATE (name), DELETE ON artists TO artist;
GRANT SELECT, INSERT, UPDATE (title, released), DELETE ON albums TO artist;
GRANT SELECT, INSERT, UPDATE (title), DELETE ON songs TO artist;
