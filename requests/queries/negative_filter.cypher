MATCH 
(p:Person)-[:KNOWN_FOR]->(w:Work)
WHERE NOT EXISTS {
    MATCH (w)-[:HAS_DIRECTOR]->(p)
}
RETURN p, w
