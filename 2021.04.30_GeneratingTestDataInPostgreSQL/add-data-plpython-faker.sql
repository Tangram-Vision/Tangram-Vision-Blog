TRUNCATE albums, artists, genres, album_genres;

CREATE EXTENSION IF NOT EXISTS plpython3u;

DO $$
    from random import randint
    from faker import Faker

    fake = Faker()

    for _ in range(6):
        plan = plpy.prepare("INSERT INTO genres (name) VALUES ($1)", ["text"])
        plan.execute([fake.street_name()])

    for _ in range(6):
        plan = plpy.prepare("INSERT INTO artists (name) VALUES ($1)", ["text"])
        plan.execute([fake.name()])

    # Alternately, we could add "RETURNING artist_id" to the above query and
    # save those values to avoid making this extra query for all artist_ids
    artist_ids = [row["artist_id"] for row in plpy.execute("SELECT artist_id FROM artists")]
    for _ in range(10):
        title = " ".join(word.title() for word in fake.words(nb=randint(1, 3)))
        plan = plpy.prepare(
            "INSERT INTO albums (artist_id, title, released) VALUES ($1, $2, $3)",
            ["int", "text", "date"],
        )
        plan.execute([random.choice(artist_ids), title, fake.date()])

    album_ids = [row["album_id"] for row in plpy.execute("SELECT album_id FROM albums")]
    genre_ids = [row["genre_id"] for row in plpy.execute("SELECT genre_id FROM genres")]
    for _ in range(15):
        plan = plpy.prepare(
            "INSERT INTO album_genres (album_id, genre_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            ["int", "int"],
        )
        plan.execute([random.choice(album_ids), random.choice(genre_ids)])
$$ LANGUAGE plpython3u;