import __init__
from py2neo import Graph
from config import NEO4J_AUTH, NEO4J_HOST

# requires: apoc.trigger.enabled=true;s

###################################################################################


def connect_neo4j() -> Graph:
    return Graph(NEO4J_HOST, auth=NEO4J_AUTH)


def create_triggers(graph: Graph) -> None:
    trigger_query = """
    CALL apoc.trigger.add(
        'logNodeCreation',
        'UNWIND $createdNodes AS n
         CREATE (log:Log {message: "Node created", nodeId: id(n), timestamp: timestamp()})',
        {phase: 'after'}
    )
    """
    graph.run(trigger_query)
    print("Created trigger: logNodeCreation")

###################################################################################


def main() -> None:
    graph = connect_neo4j()
    create_triggers(graph)


if __name__ == "__main__":
    main()
