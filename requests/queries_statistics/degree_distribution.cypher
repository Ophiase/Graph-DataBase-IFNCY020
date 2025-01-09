MATCH (n)
RETURN n.degree AS degree, count(*) AS count
ORDER BY degree DESC
