.PHONY: all download decompress process sql-load clean

DATA_DIR = data
SCRIPT = imbd_to_mysql_script.py
DB = imbd
# PG_USER = postgres

all: download decompress process sql-load clean

download:
	@mkdir -p $(DATA_DIR)
	curl -o $(DATA_DIR)/name.basics.tsv.gz https://datasets.imdbws.com/name.basics.tsv.gz
	curl -o $(DATA_DIR)/title.akas.tsv.gz https://datasets.imdbws.com/title.akas.tsv.gz
	curl -o $(DATA_DIR)/title.basics.tsv.gz https://datasets.imdbws.com/title.basics.tsv.gz
	curl -o $(DATA_DIR)/title.crew.tsv.gz https://datasets.imdbws.com/title.crew.tsv.gz
	curl -o $(DATA_DIR)/title.episode.tsv.gz https://datasets.imdbws.com/title.episode.tsv.gz
	curl -o $(DATA_DIR)/title.principals.tsv.gz https://datasets.imdbws.com/title.principals.tsv.gz
	curl -o $(DATA_DIR)/title.ratings.tsv.gz https://datasets.imdbws.com/title.ratings.tsv.gz

decompress:
	gunzip -f $(DATA_DIR)/*.tsv.gz

process:
	python $(SCRIPT)

sql-load:
	psql -d $(DB) -f output.sql

clean:
	rm -rf $(DATA_DIR)/*.tsv
