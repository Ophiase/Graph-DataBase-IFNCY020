MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, collect(w) AS works
WHERE all(work IN works WHERE work.start_year > 1950)
RETURN p, works