CALL {
    MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
    RETURN p, w
    UNION
    MATCH (p:Person)-[:HAS_DIRECTOR]->(w:Work)
    RETURN p, w
}
WHERE w.start_year > 2000
RETURN p, w
