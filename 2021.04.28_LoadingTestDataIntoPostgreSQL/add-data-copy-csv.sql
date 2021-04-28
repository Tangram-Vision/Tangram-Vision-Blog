TRUNCATE albums, artists, genres, album_genres;
COPY artists FROM '/repo/artists.csv' CSV HEADER;
COPY albums FROM '/repo/albums.csv' CSV HEADER;
COPY genres FROM '/repo/genres.csv' CSV HEADER;
COPY album_genres FROM '/repo/album_genres.csv' CSV HEADER;