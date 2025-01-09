MATCH
(p:Person {birth_year: 1975})
OPTIONAL MATCH
(p)-[:KNOWN_FOR]->(w:Work)
RETURN p, w
