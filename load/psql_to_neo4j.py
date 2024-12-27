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

@dataclass
class Akas:
    id_work: int
    ordering: int
    title: str
    region: str
    language: str
    attributes: str
    is_original_title: int

@dataclass
class Episode:
    id_work: int
    id_work_parent: int
    season_number: int
    episode_number: int

@dataclass
class Genre:
    id_work: int
    genre: str

@dataclass
class WorkType:
    id_work: int
    ordering: int
    type: str

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


def migrate_akas(pg_connect, graph) -> None:
    with pg_connect.cursor(name='akas_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, ordering, title, region, language, attributes, is_original_title
            FROM work_akas
            """)

        while True:
            akas_list = cur.fetchmany(1000)
            if not akas_list:
                break

            for akas_data in akas_list:
                akas = Akas(*akas_data)
                akas_node = Node("Akas",
                                 id_work=akas.id_work,
                                 ordering=akas.ordering,
                                 title=akas.title,
                                 region=akas.region,
                                 language=akas.language,
                                 attributes=akas.attributes,
                                 is_original_title=akas.is_original_title)
                graph.create(akas_node)
                work_node = graph.nodes.match("Work", id=akas.id_work).first()
                if work_node:
                    graph.create(Relationship(work_node, "HAS_AKAS", akas_node))
        print("Inserted akas into Neo4j")

def migrate_episode(pg_connect, graph) -> None:
    with pg_connect.cursor(name='episode_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, id_work_parent, season_number, episode_number
            FROM work_episode
            """)

        episodes = []
        while True:
            episode_batch = cur.fetchmany(1000)
            if not episode_batch:
                break
            episodes.extend(episode_batch)

        episode_nodes = {}
        for episode_data in episodes:
            episode = Episode(*episode_data)
            episode_node = Node("Episode",
                                id_work=episode.id_work,
                                id_work_parent=episode.id_work_parent,
                                season_number=episode.season_number,
                                episode_number=episode.episode_number)
            graph.create(episode_node)
            episode_nodes[(episode.id_work_parent, episode.season_number, episode.episode_number)] = episode_node

            work_node = graph.nodes.match("Work", id=episode.id_work).first()
            parent_work_node = graph.nodes.match("Work", id=episode.id_work_parent).first()

            if work_node:
                graph.create(Relationship(episode_node, "IS_WORK", work_node))
            if parent_work_node:
                graph.create(Relationship(episode_node, "IS_SUBWORK_OF", parent_work_node))

        for key, episode_node in episode_nodes.items():
            id_work_parent, season_number, episode_number = key

            if None in (id_work_parent, season_number, episode_number):
                continue
            
            next_episode_node = episode_nodes.get((id_work_parent, season_number, episode_number + 1))
            if next_episode_node:
                graph.create(Relationship(episode_node, "NEXT_EPISODE", next_episode_node))

        print("Inserted episodes into Neo4j")

def migrate_genre(pg_connect, graph) -> None:
    with pg_connect.cursor(name='genre_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, genre
            FROM work_genres
            """)

        while True:
            genres = cur.fetchmany(1000)
            if not genres:
                break

            for genre_data in genres:
                genre = Genre(*genre_data)
                genre_node = graph.nodes.match("Genre", name=genre.genre).first()
                if not genre_node:
                    genre_node = Node("Genre", name=genre.genre)
                    graph.create(genre_node)
                work_node = graph.nodes.match("Work", id=genre.id_work).first()
                if work_node:
                    graph.create(Relationship(work_node, "HAS_GENRE", genre_node))
        print("Inserted genres into Neo4j")

def migrate_work_type(pg_connect, graph) -> None:
    with pg_connect.cursor(name='work_type_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, ordering, type
            FROM work_types
            """)

        while True:
            work_types = cur.fetchmany(1000)
            if not work_types:
                break

            for work_type_data in work_types:
                work_type = WorkType(*work_type_data)
                work_type_node = graph.nodes.match("WorkType", type=work_type.type).first()
                if not work_type_node:
                    work_type_node = Node("WorkType", type=work_type.type)
                    graph.create(work_type_node)
                work_node = graph.nodes.match("Work", id=work_type.id_work).first()
                if work_node:
                    relationship = Relationship(work_node, "HAS_WORK_TYPE", work_type_node)
                    relationship["ordering"] = work_type.ordering
                    graph.create(relationship)
        print("Inserted work types into Neo4j")

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
    migrate_episode(pg_connect, graph)
    migrate_genre(pg_connect, graph)
    migrate_work_type(pg_connect, graph)
    migrate_person(pg_connect, graph)
    migrate_profession(pg_connect, graph)
    migrate_has_director(pg_connect, graph)
    migrate_has_writer(pg_connect, graph)
    migrate_known_for(pg_connect, graph)


if __name__ == "__main__":
    main()
