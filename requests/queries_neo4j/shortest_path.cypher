MATCH (start:Person {name: 'James Cagney'}), (end:Person {name: 'Lauren Bacall'})
MATCH path = shortestPath((start)-[*]-(end))
RETURN path
