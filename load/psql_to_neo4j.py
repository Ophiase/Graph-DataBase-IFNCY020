from py2neo import Graph, Node, Relationship
from psycopg2 import connect
from config import PG_DB, PG_HOST, PG_USER, PG_PASSWORD
from config import NEO4J_AUTH, NEO4J_HOST
from psql_tables import Work, Akas, Episode, Genre, WorkType, Person, Profession, Director, Writer, KnownFor

###################################################################################

MAX_FETCH_BATCH = 10000
MAX_FETCH_ITERATION = 5
VERBOSE = True
RESET = False


def main() -> None:
    pg_connect = connect_postgresql()
    graph = connect_neo4j()

    migrate_work(pg_connect, graph)
    migrate_akas(pg_connect, graph)
    migrate_episode(pg_connect, graph)
    add_next_episode(pg_connect, graph)
    migrate_genre(pg_connect, graph)
    migrate_work_type(pg_connect, graph)
    migrate_person(pg_connect, graph)
    migrate_profession(pg_connect, graph)
    migrate_has_director(pg_connect, graph)
    migrate_has_writer(pg_connect, graph)
    migrate_known_for(pg_connect, graph)

    create_indexes(graph)

###################################################################################


def connect_postgresql():
    return connect(
        dbname=PG_DB, host=PG_HOST,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def connect_neo4j() -> Graph:
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)
    if RESET:
        graph.delete_all()
    return graph


def create_indexes(graph) -> None:
    create_index(graph, "Work", "id")
    create_index(graph, "Work", "primary_title")
    create_index(graph, "Work", "original_title")
    create_index(graph, "Work", "start_year")
    create_index(graph, "Work", "end_year")
    create_index(graph, "Work", "worktype")
    
    create_index(graph, "Person", "id_person")
    create_index(graph, "Person", "name")
    create_index(graph, "Person", "birth_year")
    create_index(graph, "Person", "death_year")
    
    # create_index(graph, "Akas", "id_work")
    create_index(graph, "Akas", "title")
    create_index(graph, "Akas", "region")
    create_index(graph, "Akas", "language")
    
    create_index(graph, "Episode", "season_number")
    create_index(graph, "Episode", "episode_number")
    
    create_index(graph, "Genre", "name")
    
    create_index(graph, "WorkType", "type")
    
    create_index(graph, "Profession", "category")
    create_index(graph, "Profession", "job")


def create_index(graph, label, property) -> None:
    query = f"CREATE INDEX FOR (n:{label}) ON (n.{property})"
    graph.run(query)

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

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            works = cur.fetchmany(MAX_FETCH_BATCH)
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

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            akas_list = cur.fetchmany(MAX_FETCH_BATCH)
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
                    graph.create(Relationship(
                        work_node, "HAS_AKAS", akas_node))
        print("Inserted akas into Neo4j")


def migrate_episode(pg_connect, graph) -> None:
    with pg_connect.cursor(name='episode_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, id_work_parent, season_number, episode_number
            FROM work_episode
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            episodes = cur.fetchmany(MAX_FETCH_BATCH)
            if not episodes:
                break

            for episode_data in episodes:
                episode = Episode(*episode_data)
                episode_node = Node("Episode",
                                    season_number=episode.season_number,
                                    episode_number=episode.episode_number)
                graph.create(episode_node)
                work_node = graph.nodes.match(
                    "Work", id=episode.id_work).first()
                parent_work_node = graph.nodes.match(
                    "Work", id=episode.id_work_parent).first()
                if work_node:
                    graph.create(Relationship(
                        episode_node, "IS_WORK", work_node))
                if parent_work_node:
                    graph.create(Relationship(
                        episode_node, "IS_SUBWORK_OF", parent_work_node))

    print("Inserted episodes and relationships into Neo4j")


def add_next_episode(pg_connect, graph):
    query = """
    MATCH
    (e1:Episode)-[:IS_SUBWORK_OF]->(w:Work)<-[:IS_SUBWORK_OF]-(e2:Episode)
    WHERE 
    (e2.episode_number = e1.episode_number + 1)
    AND
    (e2.season_number = e1.season_number)
    RETURN e1, e2
    """
    result = graph.run(query)
    for record in result:
        e1 = record['e1']
        e2 = record['e2']
        graph.create(Relationship(e1, "NEXT_EPISODE", e2))
    print("Inserted NEXT_EPISODE into Neo4j")


def migrate_genre(pg_connect, graph) -> None:
    with pg_connect.cursor(name='genre_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, genre
            FROM work_genres
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            genres = cur.fetchmany(MAX_FETCH_BATCH)
            if not genres:
                break

            for genre_data in genres:
                genre = Genre(*genre_data)
                genre_node = graph.nodes.match(
                    "Genre", name=genre.genre).first()
                if not genre_node:
                    genre_node = Node("Genre", name=genre.genre)
                    graph.create(genre_node)
                work_node = graph.nodes.match("Work", id=genre.id_work).first()
                if work_node:
                    graph.create(Relationship(
                        work_node, "HAS_GENRE", genre_node))
        print("Inserted genres into Neo4j")


def migrate_work_type(pg_connect, graph) -> None:
    with pg_connect.cursor(name='work_type_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, ordering, type
            FROM work_types
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            work_types = cur.fetchmany(MAX_FETCH_BATCH)
            if not work_types:
                break

            for work_type_data in work_types:
                work_type = WorkType(*work_type_data)
                work_type_node = graph.nodes.match(
                    "WorkType", type=work_type.type).first()
                if not work_type_node:
                    work_type_node = Node("WorkType", type=work_type.type)
                    graph.create(work_type_node)
                work_node = graph.nodes.match(
                    "Work", id=work_type.id_work).first()
                if work_node:
                    relationship = Relationship(
                        work_node, "HAS_WORK_TYPE", work_type_node)
                    relationship["ordering"] = work_type.ordering
                    graph.create(relationship)
        print("Inserted work types into Neo4j")

#########################################


def migrate_person(pg_connect, graph) -> None:
    with pg_connect.cursor(name='person_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_person, name, birth_year, death_year
            FROM name_basics
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            persons = cur.fetchmany(MAX_FETCH_BATCH)
            if not persons:
                break

            for person_data in persons:
                person = Person(*person_data)
                person_node = Node("Person",
                                   id_person=person.id_person,
                                   name=person.name,
                                   birth_year=person.birth_year,
                                   death_year=person.death_year)
                graph.create(person_node)
        print("Inserted persons into Neo4j")


def migrate_profession(pg_connect, graph) -> None:
    with pg_connect.cursor(name='profession_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, ordering, id_person, category, job, characters
            FROM work_principals
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            professions = cur.fetchmany(MAX_FETCH_BATCH)
            if not professions:
                break

            for profession_data in professions:
                profession = Profession(*profession_data)
                profession_node = Node("Profession",
                                       id_work=profession.id_work,
                                       ordering=profession.ordering,
                                       id_person=profession.id_person,
                                       category=profession.category,
                                       job=profession.job,
                                       characters=profession.characters)
                graph.create(profession_node)
                work_node = graph.nodes.match(
                    "Work", id=profession.id_work).first()
                person_node = graph.nodes.match(
                    "Person", id_person=profession.id_person).first()
                if work_node and person_node:
                    graph.create(Relationship(
                        work_node, "HAS_PROFESSION", profession_node))
                    graph.create(Relationship(
                        profession_node, "BELONGS_TO", person_node))
        print("Inserted professions into Neo4j")


def migrate_has_director(pg_connect, graph) -> None:
    with pg_connect.cursor(name='director_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, id_person
            FROM work_director
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            directors = cur.fetchmany(MAX_FETCH_BATCH)
            if not directors:
                break

            for director_data in directors:
                director = Director(*director_data)
                work_node = graph.nodes.match(
                    "Work", id=director.id_work).first()
                person_node = graph.nodes.match(
                    "Person", id_person=director.id_person).first()
                if work_node and person_node:
                    graph.create(Relationship(
                        work_node, "HAS_DIRECTOR", person_node))
        print("Inserted directors into Neo4j")


def migrate_has_writer(pg_connect, graph) -> None:
    with pg_connect.cursor(name='writer_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_work, id_person
            FROM work_writer
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            writers = cur.fetchmany(MAX_FETCH_BATCH)
            if not writers:
                break

            for writer_data in writers:
                writer = Writer(*writer_data)
                work_node = graph.nodes.match(
                    "Work", id=writer.id_work).first()
                person_node = graph.nodes.match(
                    "Person", id_person=writer.id_person).first()
                if work_node and person_node:
                    graph.create(Relationship(
                        work_node, "HAS_WRITER", person_node))
        print("Inserted writers into Neo4j")


def migrate_known_for(pg_connect, graph) -> None:
    with pg_connect.cursor(name='known_for_cursor') as cur:
        cur.execute(
            """
            SELECT 
            id_person, id_work
            FROM name_known_for_titles
            """)

        for _ in range(MAX_FETCH_ITERATION):
            if VERBOSE:
                print("Fetching...")
            known_for_list = cur.fetchmany(MAX_FETCH_BATCH)
            if not known_for_list:
                break

            for known_for_data in known_for_list:
                known_for = KnownFor(*known_for_data)
                person_node = graph.nodes.match(
                    "Person", id_person=known_for.id_person).first()
                work_node = graph.nodes.match(
                    "Work", id=known_for.id_work).first()
                if person_node and work_node:
                    graph.create(Relationship(
                        person_node, "KNOWN_FOR", work_node))
        print("Inserted known_for relationships into Neo4j")

###################################################################################


if __name__ == "__main__":
    main()
