TRUNCATE albums, artists, genres, album_genres;

CREATE EXTENSION IF NOT EXISTS plpython3u;

DO $$
    print("Print statements don't appear anywhere!")

    # Manually convert value to string, quote it, and interpolate
    artist_name = plpy.quote_nullable("DJ Okawari")
    returned = plpy.execute(f"INSERT INTO artists (name) VALUES ({artist_name})")
    plpy.info(returned)  # Outputs the next line
    # INFO:  <PLyResult status=7 nrows=1 rows=[]>

    # Let PostgreSQL parameterize the query
    artist_name = "Ella Fitzgerald"
    plan = plpy.prepare("INSERT INTO artists (name) VALUES ($1) RETURNING *", ["text"])
    returned = plan.execute([artist_name])
    plpy.info(returned)  # Outputs the next line
    # INFO:  <PLyResult status=11 nrows=1 rows=[{'artist_id': 2, 'name': 'Ella Fitzgerald'}]>

    returned = plpy.execute("SELECT * FROM artists")
    plpy.info(returned)  # Outputs the next line
    # INFO:  <PLyResult status=5 nrows=2 rows=[{'artist_id': 1, 'name': 'DJ Okawari'}, {'artist_id': 2, 'name': 'Ella Fitzgerald'}]>
$$ LANGUAGE plpython3u;

