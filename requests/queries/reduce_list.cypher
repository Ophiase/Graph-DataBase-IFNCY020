MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, collect(w.runtime_minutes) AS runtimes
RETURN p, reduce(total = 0, runtime IN runtimes | total + runtime) AS total_runtime
