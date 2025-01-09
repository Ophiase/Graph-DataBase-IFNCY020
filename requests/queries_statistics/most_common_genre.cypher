MATCH (w:Work)-[:HAS_GENRE]->(g:Genre)
RETURN g.name AS genre, count(*) AS count
ORDER BY count DESC
LIMIT 1
