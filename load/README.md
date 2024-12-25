# Load

- Sources :
    - https://kxs.fr/cours/bd/imdb
        - https://kxs.fr/outils/imdb-database
            - Tables: https://datasets.imdbws.com/

I've modified `original_script_from_website.py` to `imbd_to_psql.py`.

## Installation

```bash
# Download
make download
make decompress

# to PSQL
make process
make sql-load

# to Neo4J
?
```
