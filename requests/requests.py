import sys
sys.path.append("..")
from colorama import Fore, Style, init
from load.config import NEO4J_AUTH, NEO4J_HOST
from py2neo import Graph
import os

###################################################################################

init(autoreset=True)
VERBOSE = True
QUERY_FOLDER = "queries"
LIMIT = 1

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
            print(f"{Fore.CYAN}Executing query '{name}':{Style.RESET_ALL}")
            print()
            print(limited_query)

        records = list(graph.run(limited_query))
        if not records:
            print(f"{Fore.RED}No output")
        for record in records:
            print(f"{Fore.GREEN}{record}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")

###################################################################################


if __name__ == "__main__":
    graph = connect_neo4j()
    queries = load_queries(QUERY_FOLDER)
    execute_queries(graph, queries)
