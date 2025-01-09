# 🎥 Graph DataBase IFNCY020

This project involves the creation and management of a graph database using Neo4j and PostgreSQL. \
The dataset includes information about works, persons, genres, episodes, and their relationships.

## Table of Contents

- [Loading the Dataset](#loading-the-dataset)
- [Executing Queries](#executing-queries)
- [Directory Structure](#directory-structure)

## Loading the Dataset

To load the dataset into PostgreSQL and Neo4j, follow the instructions in the [load/README.md](load/README.md) file. \
This includes steps for setting up the databases and importing the data.

## Executing Queries

The project includes a set of predefined queries for both Neo4j and PostgreSQL. These queries can be executed using the provided scripts.

To execute the queries, navigate to the `requests` directory and run the following commands:

```bash
cd requests
python3 requests_neo4j.py
python3 requests_psql.py
```

These scripts will execute the queries located in the `requests/queries_neo4j` and `requests/queries_psql` directories, respectively.

## Directory Structure

- `load/`: Contains scripts for loading the dataset into PostgreSQL and Neo4j.
- `requests/`: Contains scripts and query files for executing predefined queries.