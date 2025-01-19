from statistics import statistics

###################################################################################

QUERY_FOLDER = "queries_named_statistics"

###################################################################################

if __name__ == "__main__":
    print("Remark: You may need to execute load/named_graph.py.")
    print("Remark: The double bfs doesn't work great on directed graphs.\n")

    statistics(QUERY_FOLDER)
