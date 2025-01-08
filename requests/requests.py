import sys
import os
from py2neo import Graph
from load.config import NEO4J_AUTH, NEO4J_HOST

###################################################################################


VERBOSE = True
QUERY_FOLDER = "queries"
LIMIT = 10

###################################################################################


def connect_neo4j() -> Graph:
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)
    return graph


def load_queries(folder: str) -> dict:
    queries = {}
    for filename in os.listdir(folder):
        if filename.endswith(".cypher"):
            with open(os.path.join(folder, filename), 'r') as file:
                query = file.read().strip()
                queries[filename] = query
    return queries


def execute_queries(graph: Graph, queries: dict) -> None:
    for name, query in queries.items():
        limited_query = f"{query} LIMIT {LIMIT}"
        if VERBOSE:
            print(f"Executing query '{name}': {limited_query}")
        result = graph.run(limited_query)
        for record in result:
            print(record)

###################################################################################


if __name__ == "__main__":
    graph = connect_neo4j()
    queries = load_queries(QUERY_FOLDER)
    execute_queries(graph, queries)
