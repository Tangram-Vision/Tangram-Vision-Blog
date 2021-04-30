TRUNCATE albums, artists, genres, album_genres;

CREATE EXTENSION IF NOT EXISTS plpython3u;

DO $$
    import importlib.util

    # The second argument is the filepath on the server (inside the container)
    spec = importlib.util.spec_from_file_location("add_test_data", "/repo/add_test_data.py")
    add_test_data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(add_test_data)
    add_test_data.main(plpy)
$$ LANGUAGE plpython3u;

