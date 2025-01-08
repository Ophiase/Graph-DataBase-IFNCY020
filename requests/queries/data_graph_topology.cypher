MATCH 
p=(e1:Episode)-[:NEXT_EPISODE*10]->(e2:Episode)
RETURN p
