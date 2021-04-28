Table artists {
  artist_id int [pk, increment]
  name text
}

Table albums {
  album_id int [pk, increment]
  artist_id int
  title text
  released date
}

Table genres {
  genre_id int [pk, increment]
  name text
}

Table album_genres {
  album_id int [pk]
  genre_id int [pk]
}

Ref: artists.artist_id < albums.artist_id
Ref: albums.album_id < album_genres.album_id
Ref: genres.genre_id < album_genres.genre_id
