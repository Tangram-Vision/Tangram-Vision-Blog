TRUNCATE albums, artists, genres, album_genres;

SET plpgsql.extra_errors TO 'all';


-- Temporary tables are only accessible to the current psql session and are
-- dropped at the end of the session.
CREATE TEMPORARY TABLE words (word TEXT);

-- The WHERE clauses excludes possessive words (almost 30k of them!)
COPY words (word) FROM '/usr/share/dict/words' WHERE word NOT LIKE '%''%';

-- The SQL version of this function (see add-data-insert-random.sql) is more
-- concise, but this is how it could look when implemented in PL/pgSQL.
CREATE OR REPLACE FUNCTION generate_random_title(num_words int default 1) RETURNS text AS $$
DECLARE
  words text;
BEGIN
  SELECT initcap(array_to_string(array(
    SELECT * FROM words ORDER BY random() LIMIT num_words
  ), ' ')) INTO words;
  RETURN words;
END;
$$ LANGUAGE plpgsql;


DO $$
DECLARE
  -- Declare (and optionally assign) variables used in the below code block.
  genre_options text[] := array['Hip Hop', 'Jazz', 'Rock', 'Electronic'];
  artist_name text;
  dj_album RECORD;
BEGIN
  -- Convert each array option into a row and insert them into genres table.
  INSERT INTO genres (name) SELECT unnest(genre_options);

  FOR i IN 1..8 LOOP
    SELECT generate_random_title(ceil(random() * 2)::int) INTO artist_name;
    -- About 50% of the time, add 'DJ ' to the front of the artist's name.
    IF random() > 0.5 THEN
      artist_name = 'DJ ' || artist_name;
    END IF;
    INSERT INTO artists (name)
    SELECT artist_name;
  END LOOP;

  FOR i IN 1..6 LOOP
    INSERT INTO albums (artist_id, title, released)
    VALUES (
      (SELECT artist_id FROM artists ORDER BY random() LIMIT 1),
      (SELECT generate_random_title(ceil(random() * 2)::int)),
      (now() - '5 years'::interval * random())::date
    );
  END LOOP;

  FOR i in 1..10 LOOP
    INSERT INTO album_genres (album_id, genre_id)
    VALUES (
      (SELECT album_id FROM albums ORDER BY random() LIMIT 1),
      (SELECT genre_id FROM genres ORDER BY random() LIMIT 1)
    )
    -- If we insert a row that already exists, do nothing (don't raise an error)
    ON CONFLICT DO NOTHING;
  END LOOP;

  -- Ensure all albums by a 'DJ' artist belong to the Electronic genre.
  FOR dj_album IN
    SELECT albums.* FROM albums
    INNER JOIN artists USING (artist_id)
    WHERE artists.name LIKE 'DJ %'
  LOOP
    RAISE NOTICE 'Ensuring DJ album % belongs to Electronic genre!', quote_literal(dj_album.title);
    INSERT INTO album_genres (album_id, genre_id)
    SELECT dj_album.album_id, (SELECT genre_id FROM genres WHERE name = 'Electronic')
    -- If we insert a row that already exists, do nothing (don't raise an error)
    ON CONFLICT DO NOTHING;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

