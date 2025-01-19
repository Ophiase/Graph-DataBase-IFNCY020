import __init__
import os
from py2neo import Graph
from load.config import NEO4J_AUTH, NEO4J_HOST
from colorama import Fore, Style, init
import time

###################################################################################

init(autoreset=True)
VERBOSE = True
QUERY_FOLDER = "queries_statistics"

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


def get_statistics(graph: Graph, queries: dict) -> dict:
    stats = {}

    print("Execution times:")
    for key, query in queries.items():
        start_time = time.time()
        result = graph.run(query).data()
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"{Fore.CYAN} {key}: {Style.RESET_ALL}{execution_time:.4f} seconds")
        
        stats[key] = result[0] if result else None
    print("")

    return stats


def print_statistics(stats: dict) -> None:
    print("Results:")
    for key, value in stats.items():
        print(f"{Fore.CYAN}{key.replace('_', ' ').replace('.cypher', '').title()}: {Style.RESET_ALL}{value}")


###################################################################################

def statistics(folder: str = QUERY_FOLDER):
    graph = connect_neo4j()
    queries = load_queries(folder)
    stats = get_statistics(graph, queries)
    print_statistics(stats)


if __name__ == "__main__":
    statistics()
