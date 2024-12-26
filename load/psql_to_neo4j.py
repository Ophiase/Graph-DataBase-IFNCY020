from py2neo import Graph, Node, Relationship
from psycopg2 import connect
from config import PG_DB, PG_HOST, PG_USER, PG_PASSWORD
from config import NEO4J_AUTH, NEO4J_HOST

###################################################################################

def connect_postgresql():
    return connect(
        dbname=PG_DB, host=PG_HOST,
        user = PG_USER,
        password=PG_PASSWORD,
    )

def connect_neo4J() -> Graph:
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)
    graph.delete_all()
    return graph

###################################################################################

def migrate_films(pg_connect):
    with pg_connect.cursor() as cur:
        cur.execute(
            """
            SELECT id_work, worktype, primarytitle, originaltitle 
            FROM work_basics
            """)
        films = cur.fetchall()
        print(films[:10])

###################################################################################

def main() -> None:
    pg_connect = connect_postgresql()
    migrate_films(pg_connect)

if __name__ == "__main__":
    main()