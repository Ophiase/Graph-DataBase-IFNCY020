MATCH (p:Person)<-[:HAS_WRITER]-(w:Work)
RETURN count(DISTINCT p) AS total_writers
