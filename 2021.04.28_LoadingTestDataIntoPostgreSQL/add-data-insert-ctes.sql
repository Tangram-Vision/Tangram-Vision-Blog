TRUNCATE albums, artists, genres, album_genres;
-- In case you want to do all the INSERTs in a single statement, I guess?
WITH _genres AS (
  INSERT INTO genres (name)
  VALUES
    ('Hip Hop'),
    ('Jazz'),
    ('Electronic'),
    ('Rock'),
    ('Pop'),
    ('Funk'),
    ('Indie')
  RETURNING *
),
_artists AS (
  INSERT INTO artists (name)
  VALUES
    ('DJ Okawari'),
    ('Steely Dan'),
    ('Missy Elliott'),
    ('TWRP'),
    ('Donald Fagen'),
    ('La Luz'),
    ('Ella Fitzgerald')
  RETURNING *
),
_albums AS (
  -- Could join tables row-by-row, like https://stackoverflow.com/questions/43334603/sql-simply-join-two-tables-row-by-row
  -- But it's awkward!
  -- select * from (select row_number() over(), * from genres) as _g left outer join (select row_number() over(), * from (VALUES (...)) AS _artist_data) as _ad using (row_number);

  -- We have to specify the name a second time here, to look up the other ID. If
  -- artists have the same name, this approach fails.
  INSERT INTO albums (artist_id, title, released)
  VALUES
    ((SELECT artist_id FROM _artists WHERE name = 'DJ Okawari'), 'Mirror', '2009-06-24'),
    ((SELECT artist_id FROM _artists WHERE name = 'Steely Dan'), 'Pretzel Logic', '1974-02-20'),
    ((SELECT artist_id FROM _artists WHERE name = 'Missy Elliott'), 'Under Construction', '2002-11-12'),
    ((SELECT artist_id FROM _artists WHERE name = 'TWRP'), 'Return to Wherever', '2019-07-11'),
    ((SELECT artist_id FROM _artists WHERE name = 'Donald Fagen'), 'The Nightfly', '1982-10-01'),
    ((SELECT artist_id FROM _artists WHERE name = 'La Luz'), 'It''s Alive', '2013-10-15'),
    ((SELECT artist_id FROM _artists WHERE name = 'Ella Fitzgerald'), 'Pure Ella', '1994-02-15')
  RETURNING *
)
INSERT INTO album_genres (album_id, genre_id)
VALUES
  ((SELECT artist_id FROM _albums WHERE title = 'Mirror'), (SELECT genre_id FROM _genres WHERE name = 'Hip Hop')),
  ((SELECT artist_id FROM _albums WHERE title = 'Mirror'), (SELECT genre_id FROM _genres WHERE name = 'Jazz')),
  ((SELECT artist_id FROM _albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM _genres WHERE name = 'Jazz')),
  ((SELECT artist_id FROM _albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM _genres WHERE name = 'Rock')),
  ((SELECT artist_id FROM _albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM _genres WHERE name = 'Pop')),
  ((SELECT artist_id FROM _albums WHERE title = 'Under Construction'), (SELECT genre_id FROM _genres WHERE name = 'Hip Hop')),
  ((SELECT artist_id FROM _albums WHERE title = 'Return to Wherever'), (SELECT genre_id FROM _genres WHERE name = 'Rock')),
  ((SELECT artist_id FROM _albums WHERE title = 'Return to Wherever'), (SELECT genre_id FROM _genres WHERE name = 'Funk')),
  ((SELECT artist_id FROM _albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM _genres WHERE name = 'Jazz')),
  ((SELECT artist_id FROM _albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM _genres WHERE name = 'Rock')),
  ((SELECT artist_id FROM _albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM _genres WHERE name = 'Pop')),
  ((SELECT artist_id FROM _albums WHERE title = 'It''s Alive'), (SELECT genre_id FROM _genres WHERE name = 'Indie')),
  ((SELECT artist_id FROM _albums WHERE title = 'Pure Ella'), (SELECT genre_id FROM _genres WHERE name = 'Jazz'));
