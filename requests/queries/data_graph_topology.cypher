MATCH (e1:Episode)-[:NEXT_EPISODE*]->(e2:Episode)
WHERE e1.season_number = 1 AND e2.season_number = 1
RETURN e1, e2
