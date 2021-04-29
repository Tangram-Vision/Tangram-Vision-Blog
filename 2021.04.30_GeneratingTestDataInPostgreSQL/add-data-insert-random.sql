TRUNCATE albums, artists, genres, album_genres;

-- Temporary tables are only accessible to the current psql session and are
-- dropped at the end of the session.
CREATE TEMPORARY TABLE words (word TEXT);

-- The WHERE clauses excludes possessive words (almost 30k of them!)
COPY words (word) FROM '/usr/share/dict/words' WHERE word NOT LIKE '%''%';

-- Use 8 random hex chars as the genre name.
INSERT INTO genres (name)
SELECT substr(md5(random()::text), 1, 8) FROM generate_series(1, 5) AS _g;

INSERT INTO artists (name)
SELECT
  -- Pick one random word as the artist name.
  (SELECT * FROM words ORDER BY random() LIMIT 1)
FROM generate_series(1, 4) AS _g;

INSERT INTO albums (artist_id, title, released)
SELECT
  -- Select a random artist from the artists table.
  -- NOTE: random() is only evaluated once in this subquery unless it depends on
  -- the outer query, hence the "_g*0" after random().
  (SELECT artist_id FROM artists ORDER BY random()+_g*0 LIMIT 1),

  -- Select the first 1-3 rows after randomly sorting the word list, then join
  -- them with spaces between each word and capitalize the first letter of each
  -- word.
  initcap(array_to_string(array(
    SELECT * FROM words ORDER BY random()+_g*0 LIMIT ceil(random() * 3)
  ), ' ')),

  -- Subtract between 0-5 years from today as the album release date.
  (now() - '5 years'::interval * random())::date
FROM generate_series(1, 8) AS _g;

-- Assign a random album a random genre. Repeat 10 times.
INSERT INTO album_genres (album_id, genre_id)
SELECT
  (SELECT album_id FROM albums ORDER BY random()+_g*0 LIMIT 1),
  (SELECT genre_id FROM genres ORDER BY random()+_g*0 LIMIT 1)
FROM generate_series(1, 10) AS _g
-- If we insert a row that already exists, do nothing (don't raise an error)
ON CONFLICT DO NOTHING;