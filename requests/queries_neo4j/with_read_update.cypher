MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, w
WHERE w.start_year < 2000
SET p:Veteran
RETURN p, w
