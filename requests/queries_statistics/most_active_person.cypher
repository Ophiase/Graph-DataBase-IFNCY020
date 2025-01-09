MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
RETURN p.name AS person, count(*) AS count
ORDER BY count DESC
LIMIT 1
