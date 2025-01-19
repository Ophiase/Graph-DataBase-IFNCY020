import sys
from py2neo import Graph
from py2neo.errors import ClientError
from config import NEO4J_AUTH, NEO4J_HOST

###################################################################################

VERBOSE = False

#########################################


def connect_neo4j() -> Graph:
    return Graph(NEO4J_HOST, auth=NEO4J_AUTH)


def create_named_graph(graph) -> None:
    queries = {
        'Graph': """
            CALL gds.graph.project(
            'Graph', 
            '*', 
            '*');
        """,
        'WorkGraph': """
            CALL gds.graph.project(
                'WorkGraph',
                {
                    Work: {
                        properties: ['id', 'start_year', 'end_year'] 
                    }
                },
                {
                    HAS_GENRE: {
                        orientation: 'UNDIRECTED'
                    },
                    HAS_DIRECTOR: {
                        orientation: 'UNDIRECTED'
                    },
                    HAS_WRITER: {
                        orientation: 'UNDIRECTED'
                    }
                }
            );
            """,
        'PersonGraph': """
            CALL gds.graph.project(
                'PersonGraph',
                {
                    Person: {
                        properties: ['id_person', 'birth_year', 'death_year']
                    }
                },
                {
                    BELONGS_TO: {
                        orientation: 'UNDIRECTED'
                    },
                    KNOWN_FOR: {
                        orientation: 'UNDIRECTED'
                    }
                }
            );
            """
    }

    for graph_name, query in queries.items():
        print(f"Creating a named graph '{graph_name}'")
        if VERBOSE:
            print(f"\n{query}")
        try:
            graph.run(query)
        except ClientError as e:
            if "already exists" in str(e):
                print("\tGraph already exists")
            else:
                print("\n" + repr(e))
        print(f"{ '-' * 30 }\n")

###################################################################################


def main() -> None:
    create_named_graph(connect_neo4j())


if __name__ == "__main__":
    main()
