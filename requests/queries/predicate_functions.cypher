MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WHERE all(work IN collect(w) WHERE work.start_year > 2000)
RETURN p, w