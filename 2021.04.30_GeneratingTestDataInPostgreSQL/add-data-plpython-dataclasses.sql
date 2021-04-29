TRUNCATE albums, artists, genres, album_genres;

CREATE EXTENSION IF NOT EXISTS plpython3u;

DO $$
    from dataclasses import dataclass, field
    import datetime
    from random import randint, choice
    from typing import List, Any, Type, TypeVar

    from faker import Faker


    T = TypeVar("T", bound="DataGeneratorBase")
    fake = Faker()


    # This is a useful base class for tracking instances so we can use them in
    # relationships (picking a random artist or genre to foreign key to).
    class DataGeneratorBase:
        def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
            "Track class instances in a list on the class"
            instance = super().__new__(cls, *args, **kwargs)  # type: ignore
            if "instances" not in cls.__dict__:
                cls.instances = []
            cls.instances.append(instance)
            return instance


    @dataclass
    class Genre(DataGeneratorBase):
        genre_id: int = field(init=False)
        name: str = field(default_factory=fake.street_name)


    @dataclass
    class Artist(DataGeneratorBase):
        artist_id: int = field(init=False)
        name: str = field(default_factory=fake.name)


    @dataclass
    class Album(DataGeneratorBase):
        album_id: int = field(init=False)
        artist: Artist = field(default_factory=lambda: choice(Artist.instances))
        title: str = field(
            default_factory=lambda: " ".join(
                word.title() for word in fake.words(nb=randint(1, 3))
            )
        )
        released: datetime.date = field(default_factory=fake.date)
        genres: List[Genre] = field(
            # Use Faker to pick a list of genres to avoid duplicates
            default_factory=lambda: fake.random_elements(Genre.instances, length=randint(0, 3), unique=True)
        )


    for _ in range(6):
        g = Genre()
        # "RETURNING id" lets us get the database-generated and store it on the
        # Python object for later reference without needing to issue additional
        # queries.
        plan = plpy.prepare(
            "INSERT INTO genres (name) VALUES ($1) RETURNING genre_id", ["text"]
        )
        g.genre_id = plan.execute([g.name])[0]["genre_id"]
    for _ in range(6):
        artist = Artist()
        plan = plpy.prepare(
            "INSERT INTO artists (name) VALUES ($1) RETURNING artist_id", ["text"]
        )
        artist.artist_id = plan.execute([artist.name])[0]["artist_id"]
    for _ in range(8):
        album = Album()
        plan = plpy.prepare(
            "INSERT INTO albums (artist_id, title, released) VALUES ($1, $2, $3) RETURNING album_id",
            ["int", "text", "date"],
        )
        album.album_id = plan.execute(
            [album.artist.artist_id, album.title, album.released]
        )[0]["album_id"]

        # Insert album_genres rows
        for g in album.genres:
            plan = plpy.prepare(
                "INSERT INTO album_genres (album_id, genre_id) VALUES ($1, $2)",
                ["int", "int"],
            )
            plan.execute([album.album_id, g.genre_id])
$$ LANGUAGE plpython3u;

