MATCH (p:Person)-[:HAS_DIRECTOR]->(w:Work)
RETURN count(DISTINCT p) AS total_directors
