from py2neo import Graph, Node, Relationship
from psycopg2 import connect
from config import PG_DB, PG_HOST, PG_USER, PG_PASSWORD
from config import NEO4J_AUTH, NEO4J_HOST
from dataclasses import dataclass

###################################################################################


@dataclass
class Work:
    id: int
    worktype: str
    primary_title: str
    original_title: str
    is_adult: int
    start_year: int
    end_year: int
    runtime_minutes: int

###################################################################################


def connect_postgresql():
    return connect(
        dbname=PG_DB, host=PG_HOST,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def connect_neo4j() -> Graph:
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)
    graph.delete_all()
    return graph

###################################################################################


def migrate_work(pg_connect, graph) -> None:
    with pg_connect.cursor(name='work_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, worktype, primary_title, original_title,
            is_adult, start_year, end_year, runtime_minutes
            FROM work_basics
            """)

        while True:
            print("Fetching...")
            works = cur.fetchmany(1000)
            if not works:
                break

            for work_data in works:
                work = Work(*work_data)
                work_node = Node("Work",
                                 id=work.id,
                                 worktype=work.worktype,
                                 primary_title=work.primary_title,
                                 original_title=work.original_title,
                                 is_adult=work.is_adult,
                                 start_year=work.start_year,
                                 end_year=work.end_year,
                                 runtime_minutes=work.runtime_minutes)
                work_node.__primarylabel__ = "Work"
                work_node.__primarykey__ = "id"
                work_node._id = "id"
                graph.create(work_node)
        print("Inserted works into Neo4j")


def migrate_akas(pg_connect, graph) -> None: pass
"""
            SELECT 
            id_work, ordering, title, region, language, attributes, is_original_title
            FROM work_akas
            """
# for this one, you will create a NodeType Akas
# then create the relation (:Work)-[:HAS_AKAS]->(:Akas)

def migrate_episode(pg_connect, graph) -> None: pass
"""
            SELECT 
            id_work, id_work_parent, season_number, episode_number
            FROM work_episode
            """
# for this one, you will create a nodeType Episode (it seems that every episode have their own id_work)
# then create the relations 
#   (:Episode)-[:IsWork]->(:Work)
#   (:Episode)-[:IsSubWorkOf]->(:Work)
#   (:Episode)-[:NextEpisode or :LastEpisode]->(:Episode)
#       # pick the easiest between Next and Last
#       # you need to find the episode with number +- 1 of episode in the same seaosn with same id_work_parent




def migrate_genre(pg_connect, graph) -> None: pass
"""
            SELECT 
            id_work, genre
            FROM work_genres
            """
# create (:Work)-[:HasGenre]->(:Genre)
# do not create twice a :Genre, re-use one if you already have created it

def migrate_work_type(pg_connect, graph) -> None: pass
"""
            SELECT 
            id_work, ordering, type
            FROM work_genres
            """
# create (:Work)-[:HasWorkType]->(:WorkType)
# do not create twice a :WorkType, re-use one if you already have created it
    # but the :HasWorkType should have the attribute "ordering"

#########################################


def migrate_person(pg_connect, graph) -> None: pass


def migrate_profession(pg_connect, graph) -> None: pass

#########################################


def migrate_has_director(pg_connect, graph) -> None: pass


def migrate_has_writer(pg_connect, graph) -> None: pass


def migrate_known_for(pg_connect, graph) -> None: pass

###################################################################################


def main() -> None:
    pg_connect = connect_postgresql()
    graph = connect_neo4j()

    migrate_work(pg_connect, graph)
    migrate_akas(pg_connect, graph)
    migrate_genre(pg_connect, graph)
    migrate_genre(pg_connect, graph)
    migrate_work_type(pg_connect, graph)
    migrate_person(pg_connect, graph)
    migrate_profession(pg_connect, graph)
    migrate_has_director(pg_connect, graph)
    migrate_has_writer(pg_connect, graph)
    migrate_known_for(pg_connect, graph)


if __name__ == "__main__":
    main()
