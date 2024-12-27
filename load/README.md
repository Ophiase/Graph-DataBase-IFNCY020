# Load


- Postgres tables
    - ![](resources/tables.png)
- Neo4J structure:
    - ?

- Sources :
    - https://kxs.fr/cours/bd/imdb
        - https://kxs.fr/outils/imdb-database
            - Tables: https://datasets.imdbws.com/
    - Remark: I've modified `original_script_from_website.py` to `imbd_to_psql.py`.

## Installation

```bash
# To execute all the following commands once
make all

# Download
make download
make decompress

# Glimpse to raw data
make glimpse

# to PSQL
make psql_load
make psql_to_neo4j

# to Neo4J
make psql_to_neo4j
```
