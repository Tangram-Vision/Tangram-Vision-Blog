TRUNCATE albums, artists, genres, album_genres;
INSERT INTO genres (genre_id, name)
OVERRIDING SYSTEM VALUE
VALUES
  (1, 'Hip Hop'),
  (2, 'Jazz'),
  (3, 'Electronic'),
  (4, 'Rock'),
  (5, 'Pop'),
  (6, 'Funk'),
  (7, 'Indie');

INSERT INTO artists (artist_id, name)
OVERRIDING SYSTEM VALUE
VALUES
  (1, 'DJ Okawari'),
  (2, 'Steely Dan'),
  (3, 'Missy Elliott'),
  (4, 'TWRP'),
  (5, 'Donald Fagen'),
  (6, 'La Luz'),
  (7, 'Ella Fitzgerald');

INSERT INTO albums (album_id, artist_id, title, released)
OVERRIDING SYSTEM VALUE
VALUES
  (1, 1, 'Mirror', '2009-06-24'),
  (2, 2, 'Pretzel Logic', '1974-02-20'),
  (3, 3, 'Under Construction', '2002-11-12'),
  (4, 4, 'Return to Wherever', '2019-07-11'),
  (5, 5, 'The Nightfly', '1982-10-01'),
  (6, 6, 'It''s Alive', '2013-10-15'),
  (7, 7, 'Pure Ella', '1994-02-15');

INSERT INTO album_genres (album_id, genre_id)
VALUES
  (1, 1),
  (1, 2),
  (2, 2),
  (2, 4),
  (2, 5),
  (3, 1),
  (4, 4),
  (4, 6),
  (5, 2),
  (5, 4),
  (5, 5),
  (6, 7),
  (7, 2);