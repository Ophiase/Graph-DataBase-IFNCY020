MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, count(w) AS workCount
WHERE workCount > 5
RETURN p, workCount
