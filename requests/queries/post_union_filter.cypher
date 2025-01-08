CALL {
    MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
    WHERE w.start_year > 1940
    RETURN p, w
    UNION
    MATCH (p:Person)-[:HAS_DIRECTOR]->(w:Work)
    WHERE w.start_year > 1940
    RETURN p, w
}
RETURN p, w
