FROM postgres:13

COPY requirements.txt /requirements.txt
COPY dict-american-english /usr/share/dict/words
RUN set -eux; \
    apt-get update && apt-get install -y \
      # For plpython3u extension, for generating test data
      python3 \
      python3-pip \
      postgresql-plpython3-$PG_MAJOR; \
    # Install pip dependencies for generating test data
    pip3 install -r /requirements.txt; \
    rm -rf /var/lib/apt/lists/*;

# ENTRYPOINT and CMD will be inherited from postgres image