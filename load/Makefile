.PHONY: all download decompress process sql-load clean

###################################################################################

DATA_DIR = data
SCRIPT = imbd_to_psql.py
SQL_SCRIPT = script.sql
DB = imbd

###################################################################################

all: download_and_decompress glimpse tsv_to_psql # clean
download_and_decompress: download decompress
tsv_to_psql: process sql-load

###################################################################################

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
	cd data; psql -d $(DB) -f $(SQL_SCRIPT)

glimpse:
	mkdir -p resume
	for file in data/*.tsv; do head -20 "$$file" > "resume/$$(basename $$file)"; done

clean:
	rm -rf $(DATA_DIR)/*.tsv
