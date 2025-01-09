MATCH (e:Episode)-[:NEXT_EPISODE*]->(e2:Episode)
RETURN e, e2
