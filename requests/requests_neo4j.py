import __init__
import os
from py2neo import Graph
from load.config import NEO4J_AUTH, NEO4J_HOST
from colorama import Fore, Style, init
import time


###################################################################################

init(autoreset=True)
VERBOSE = True
QUERY_FOLDER = "queries_neo4j"
LIMIT = 1
DISABLED = [
    "weighted_dijkstra.cypher" # TODO: fix
]

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
        if name in DISABLED:
            print(f"Skip {name}")
            continue

        limited_query = f"{query} LIMIT {LIMIT}"
        if VERBOSE:
            print(f"{Fore.CYAN}Executing query '{name}':{Style.RESET_ALL}")
            print()
            print(limited_query)
            print()
            start_time = time.time()

            records = list(graph.run(limited_query))

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{Fore.MAGENTA}Execution time: {execution_time:.4f} seconds{Style.RESET_ALL}")
        if not records:
            print(f"{Fore.RED}No output")
        for record in records:
            print(f"{Fore.GREEN}{record}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")

###################################################################################


if __name__ == "__main__":
    print("""Warning:
          If a request return "No output". 
          It suggest that you didn't fill enough the database.
          My parameters in psql_to_neo4j:
            MAX_FETCH_BATCH = 10000
            MAX_FETCH_ITERATION = 10
          
          """)
    print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")

    graph = connect_neo4j()
    queries = load_queries(QUERY_FOLDER)
    execute_queries(graph, queries)
