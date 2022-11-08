-- Add 3 musical artists
INSERT INTO artists (name)
    VALUES ('Tupper Ware Remix Party'), ('Steely Dan'), ('Missy Elliott');

-- Switch to the artist role (so we're not querying from a superuser role, which
-- bypasses RLS)
SET ROLE artist;

SELECT * FROM artists;
--  artist_id |          name
-- -----------+-------------------------
--          1 | Tupper Ware Remix Party
--          2 | Steely Dan
--          3 | Missy Elliott
-- (3 rows)

-- Switch to the postgres superuser to enable RLS on the artists table
RESET ROLE;
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;

-- Now we don't see any rows! RLS hides all rows if no policies are declared on
-- the table.
SET ROLE artist;
SELECT * FROM artists;
--  artist_id | name
-- -----------+------
-- (0 rows)

-- Let's create a simple RLS policy that applies to all roles and commands and
-- allows access to all rows.
RESET ROLE;
CREATE POLICY testing ON artists
    USING (true);

-- The expression "true" is true for all rows, so all rows are visible.
SET ROLE artist;
SELECT * FROM artists;
--  artist_id |          name
-- -----------+-------------------------
--          1 | Tupper Ware Remix Party
--          2 | Steely Dan
--          3 | Missy Elliott
-- (3 rows)

-- Let's change the policy to use an expression that depends on a value in the
-- row.
RESET ROLE;
ALTER POLICY testing ON artists
    USING (name = 'Steely Dan');

-- Now, we see that only 1 row passes the policy's test.
SET ROLE artist;
SELECT * FROM artists;
--  artist_id |    name
-- -----------+------------
--          2 | Steely Dan
-- (1 row)

RESET ROLE;
-- Create a login/role for a specific artist. We'll design the role name to be
-- "artist:N" where N is the artist_id. So, "artist:1" will be the account for
-- Tupper Ware Remix Party.
-- NOTE: We have to quote the role name because it contains a colon.
CREATE ROLE "artist:1" LOGIN;
GRANT artist TO "artist:1";

-- Let's make all artists visible to all users again
DROP POLICY testing ON artists;
CREATE POLICY viewable_by_all ON artists
    FOR SELECT
    USING (true);

-- We create an RLS policy specific to the "artist" role/group and the UPDATE
-- command. The policy makes rows from the "artists" table available if the
-- row's artist_id matches the number in the current user's name (i.e.
-- a db role name of "artist:1" makes the row with artist_id=1 available).
CREATE POLICY update_self ON artists
    FOR UPDATE
    TO artist
    USING (artist_id = substr(current_user, 8)::int);

SET ROLE "artist:1";
-- Even though we try to update the name for all artists in the table, the RLS
-- policy limits our update to only the row we "own" (i.e. that has an artist_id
-- matching our db role name).
UPDATE artists SET name = 'TWRP';
-- UPDATE 1
SELECT * FROM artists;
--  artist_id |     name
-- -----------+---------------
--          2 | Steely Dan
--          3 | Missy Elliott
--          1 | TWRP
-- (3 rows)

-- Trying to update a row that no policy gives us access to simply results in no
-- rows updating.
UPDATE artists SET name = 'Ella Fitzgerald' WHERE name = 'Steely Dan';
-- UPDATE 0


RESET ROLE;
-- Enable RLS on albums and songs, and make them viewable by everyone.
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;
ALTER TABLE songs ENABLE ROW LEVEL SECURITY;
CREATE POLICY viewable_by_all ON albums
    FOR SELECT
    USING (true);
CREATE POLICY viewable_by_all ON songs
    FOR SELECT
    USING (true);

-- Limit create/edit/delete of albums to the "owning" artist.
CREATE POLICY affect_own_albums ON albums
    FOR ALL
    TO artist
    USING (artist_id = substr(current_user, 8)::int);
-- Limit create/edit/delete of songs to the "owning" artist of the album.
CREATE POLICY affect_own_songs ON songs
    FOR ALL
    TO artist
    USING (
        -- Alternative:
        -- (SELECT artist_id FROM albums WHERE songs.album_id = album_id
        -- ) = substr(current_user, 8)::int
        --
        -- Alternative:
        -- (SELECT artist_id = substr(current_user, 8)::int
        -- FROM albums WHERE albums.album_id = songs.album_id)
        --
        --
        EXISTS (
            SELECT 1 FROM albums
            WHERE albums.album_id = songs.album_id
            AND albums.artist_id = substr(current_user, 8)::int
        )
    );

-- Add a Missy Elliott (artist_id=3) album (album_id=1) for testing below
INSERT INTO albums (artist_id, title, released)
    VALUES (3, 'Under Construction', '2002-11-12');

-- Change to the user account corresponding to the artist TWRP (artist_id=1)
SET ROLE "artist:1";
-- Add an album (album_id=2) and a song to that album
INSERT INTO albums (artist_id, title, released)
    VALUES (1, 'Return to Wherever', '2019-07-11');
INSERT INTO songs (album_id, title)
    VALUES (2, 'Hidden Potential');

-- Trying to add an album to another artist fails the RLS policy
INSERT INTO albums (artist_id, title, released)
    VALUES (2, 'Pretzel Logic', '1974-02-20');
-- ERROR:  42501: new row violates row-level security policy for table "albums"
-- LOCATION:  ExecWithCheckOptions, execMain.c:2058

-- Trying to add a song to Missy Elliott's album fails the RLS policy
INSERT INTO songs (album_id, title)
    VALUES (1, 'Work It');
-- ERROR:  42501: new row violates row-level security policy for table "songs"
-- LOCATION:  ExecWithCheckOptions, execMain.c:2058


-- Insert an album (album_id=4) with a future release date
INSERT INTO albums (artist_id, title, released)
    VALUES (1, 'Future Album', '2050-01-01');
INSERT INTO songs (album_id, title)
    VALUES (4, 'Future Song 1');


-- Allow artists to create albums with a future release date, but only the
-- owning artist should be able to see these not-yet-released albums.

RESET ROLE;
-- Reminder: We previously created a viewable_by_all policy on albums that shows
-- all rows to SELECT queries issued by all roles. We re-create that policy here
-- for reference:
DROP POLICY viewable_by_all ON albums;
CREATE POLICY viewable_by_all ON albums
    FOR SELECT
    USING (true);
-- For fans: restrict visibility to albums with a release date in the past.
CREATE POLICY hide_unreleased_from_fans ON albums
    AS RESTRICTIVE
    FOR SELECT
    TO fan
    USING (released <= now());
-- For artists: restrict visibility to albums with a release date in the past,
-- unless the role issuing the query is the owning artist.
CREATE POLICY hide_unreleased_from_other_artists ON albums
    AS RESTRICTIVE
    FOR SELECT
    TO artist
    USING (released <= now() or (artist_id = substr(current_user, 8)::int));

-- Alternate implementation using only PERMISSIVE (rather than RESTRICTIVE)
-- policies.
DROP POLICY viewable_by_all ON albums;
DROP POLICY hide_unreleased_from_fans ON albums;
DROP POLICY hide_unreleased_from_other_artists ON albums;
CREATE POLICY viewable_by_all ON albums
    FOR SELECT
    USING (released <= now());
-- Reminder: We previously created an affect_own_albums policy on albums that
-- already allows the artist to see their own albums. We re-create that policy
-- here for reference:
DROP POLICY affect_own_albums ON albums;
CREATE POLICY affect_own_albums ON albums
    -- FOR ALL
    TO artist
    USING (artist_id = substr(current_user, 8)::int);


-- To control visibility of songs, we simply query for the corresponding album
-- and the RLS policy on the albums table will determine if we can see the
-- album. If we see the album, we'll see the songs.
DROP POLICY viewable_by_all ON songs;
CREATE POLICY viewable_by_all ON songs
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM albums
            WHERE albums.album_id = songs.album_id
        )
    );


-- Create another artist role for testing
CREATE ROLE "artist:2";
GRANT artist TO "artist:2";

-- Test that the owning artist can see future albums and songs, but other
-- artists and fans cannot see them.
SET ROLE "artist:1";
SELECT * FROM albums;
--  album_id | artist_id |       title        |  released
-- ----------+-----------+--------------------+------------
--         1 |         3 | Under Construction | 2002-11-12
--         2 |         1 | Return to Wherever | 2019-07-11
--         4 |         1 | Secret Project     | 2050-01-01
-- (3 rows)

SELECT * FROM songs;
--  song_id | album_id |      title
-- ---------+----------+------------------
--        1 |        2 | Hidden Potential
--        4 |        4 | Untitled Song 1
-- (2 rows)

SET ROLE fan;
SELECT * FROM albums;
--  album_id | artist_id |       title        |  released
-- ----------+-----------+--------------------+------------
--         1 |         3 | Under Construction | 2002-11-12
--         2 |         1 | Return to Wherever | 2019-07-11
-- (2 rows)

SELECT * FROM songs;
--  song_id | album_id |      title
-- ---------+----------+------------------
--        1 |        2 | Hidden Potential
-- (1 row)

SET ROLE "artist:2";
SELECT * FROM albums;
--  album_id | artist_id |       title        |  released
-- ----------+-----------+--------------------+------------
--         1 |         3 | Under Construction | 2002-11-12
--         2 |         1 | Return to Wherever | 2019-07-11
-- (2 rows)

SELECT * FROM songs;
--  song_id | album_id |      title
-- ---------+----------+------------------
--        1 |        2 | Hidden Potential
-- (1 row)
