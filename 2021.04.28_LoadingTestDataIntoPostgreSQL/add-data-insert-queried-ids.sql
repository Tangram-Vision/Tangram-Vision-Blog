TRUNCATE albums, artists, genres, album_genres;
INSERT INTO genres (name)
VALUES
  ('Hip Hop'),
  ('Jazz'),
  ('Electronic'),
  ('Rock'),
  ('Pop'),
  ('Funk'),
  ('Indie');

INSERT INTO artists (name)
VALUES
  ('DJ Okawari'),
  ('Steely Dan'),
  ('Missy Elliott'),
  ('TWRP'),
  ('Donald Fagen'),
  ('La Luz'),
  ('Ella Fitzgerald');

INSERT INTO albums (artist_id, title, released)
VALUES
  ((SELECT artist_id FROM artists WHERE name = 'DJ Okawari'), 'Mirror', '2009-06-24'),
  ((SELECT artist_id FROM artists WHERE name = 'Steely Dan'), 'Pretzel Logic', '1974-02-20'),
  ((SELECT artist_id FROM artists WHERE name = 'Missy Elliott'), 'Under Construction', '2002-11-12'),
  ((SELECT artist_id FROM artists WHERE name = 'TWRP'), 'Return to Wherever', '2019-07-11'),
  ((SELECT artist_id FROM artists WHERE name = 'Donald Fagen'), 'The Nightfly', '1982-10-01'),
  ((SELECT artist_id FROM artists WHERE name = 'La Luz'), 'It''s Alive', '2013-10-15'),
  ((SELECT artist_id FROM artists WHERE name = 'Ella Fitzgerald'), 'Pure Ella', '1994-02-15');

INSERT INTO album_genres (album_id, genre_id)
VALUES
  ((SELECT album_id FROM albums WHERE title = 'Mirror'), (SELECT genre_id FROM genres WHERE name = 'Hip Hop')),
  ((SELECT album_id FROM albums WHERE title = 'Mirror'), (SELECT genre_id FROM genres WHERE name = 'Jazz')),
  ((SELECT album_id FROM albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM genres WHERE name = 'Jazz')),
  ((SELECT album_id FROM albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM genres WHERE name = 'Rock')),
  ((SELECT album_id FROM albums WHERE title = 'Pretzel Logic'), (SELECT genre_id FROM genres WHERE name = 'Pop')),
  ((SELECT album_id FROM albums WHERE title = 'Under Construction'), (SELECT genre_id FROM genres WHERE name = 'Hip Hop')),
  ((SELECT album_id FROM albums WHERE title = 'Return to Wherever'), (SELECT genre_id FROM genres WHERE name = 'Rock')),
  ((SELECT album_id FROM albums WHERE title = 'Return to Wherever'), (SELECT genre_id FROM genres WHERE name = 'Funk')),
  ((SELECT album_id FROM albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM genres WHERE name = 'Jazz')),
  ((SELECT album_id FROM albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM genres WHERE name = 'Rock')),
  ((SELECT album_id FROM albums WHERE title = 'The Nightfly'), (SELECT genre_id FROM genres WHERE name = 'Pop')),
  ((SELECT album_id FROM albums WHERE title = 'It''s Alive'), (SELECT genre_id FROM genres WHERE name = 'Indie')),
  ((SELECT album_id FROM albums WHERE title = 'Pure Ella'), (SELECT genre_id FROM genres WHERE name = 'Jazz'));