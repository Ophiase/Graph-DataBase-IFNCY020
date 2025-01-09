MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, collect(w) AS works
UNWIND works AS work
RETURN p, work
