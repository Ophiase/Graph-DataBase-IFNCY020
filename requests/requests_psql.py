import __init__
import os
from psycopg2 import connect
from load.config import PG_DB, PG_HOST, PG_USER, PG_PASSWORD
from colorama import Fore, Style, init


###################################################################################

init(autoreset=True)
VERBOSE = True
QUERY_FOLDER = "queries_psql"
LIMIT = 3

###################################################################################


def connect_postgresql():
    return connect(
        dbname=PG_DB, host=PG_HOST,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def load_queries(folder: str) -> dict:
    queries = {}
    for filename in os.listdir(folder):
        if filename.endswith(".sql"):
            with open(os.path.join(folder, filename), 'r') as file:
                query = file.read().strip()
                queries[filename] = query
    return queries


def execute_queries(pg_connect, queries: dict) -> None:
    with pg_connect.cursor() as cur:
        for name, query in queries.items():
            limited_query = f"{query} \nLIMIT {LIMIT}"
            if VERBOSE:
                print(f"{Fore.CYAN}Executing query '{name}':{Style.RESET_ALL}")
                print()
                print(limited_query)
                print()

            cur.execute(limited_query)
            records = cur.fetchall()
            if not records:
                print(f"{Fore.RED}No output")
            for record in records:
                print(f"{Fore.GREEN}{record}{Style.RESET_ALL}")

            print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")

###################################################################################


if __name__ == "__main__":
    pg_connect = connect_postgresql()
    queries = load_queries(QUERY_FOLDER)
    execute_queries(pg_connect, queries)
