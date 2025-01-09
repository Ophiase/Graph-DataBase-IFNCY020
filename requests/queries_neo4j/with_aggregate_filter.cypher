MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, count(w) AS workCount
WHERE workCount >= 4
RETURN p, workCount
