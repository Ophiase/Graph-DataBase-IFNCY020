from py2neo import Graph
from config import NEO4J_AUTH, NEO4J_HOST, DUMP

###################################################################################


def dump_neo4j_database(output_file):
    graph = Graph(NEO4J_HOST, auth=NEO4J_AUTH)

    print("load statistics")

    total_nodes = graph.evaluate("MATCH (n) RETURN count(n)")
    total_relationships = graph.evaluate("MATCH ()-[r]->() RETURN count(r)")
    total_records = total_nodes + total_relationships

    print("begin..")

    with open(output_file, 'w') as file:
        count = 0
        last_percentage = 0
        for record in graph.run("MATCH (n) RETURN n"):
            file.write(f"{record['n']}\n")
            count += 1
            percentage = int(count / total_records * 100)
            if percentage >= last_percentage + 5:
                print(f"Progress: {percentage}%")
                last_percentage = percentage

        for record in graph.run("MATCH ()-[r]->() RETURN r"):
            file.write(f"{record['r']}\n")
            count += 1
            percentage = int(count / total_records * 100)
            if percentage >= last_percentage + 5:
                print(f"Progress: {percentage}%")
                last_percentage = percentage

###################################################################################


def main() -> None:
    dump_neo4j_database(DUMP)


if __name__ == "__main__":
    main()
