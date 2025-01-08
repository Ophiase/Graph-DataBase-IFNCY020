from py2neo import Graph
from config import NEO4J_AUTH, NEO4J_HOST, DUMP

###################################################################################


def load_neo4j_database(input_file):
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)

    with open(input_file, 'r') as file:
        data = file.readlines()

    total_lines = len(data)
    count = 0
    last_percentage = 0

    tx = graph.begin()
    for line in data:
        if '->' in line:
            tx.run(f"CREATE {line.strip()}")
        else:
            tx.run(f"CREATE {line.strip()}")
        count += 1
        percentage = int(count / total_lines * 100)
        if percentage >= last_percentage + 5:
            print(f"Progress: {percentage}%")
            last_percentage = percentage
    tx.commit()


if __name__ == "__main__":
    load_neo4j_database(DUMP)
