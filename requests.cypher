// Query with a negative filter on certain types of patterns (absence of a certain pattern)

MATCH 
(p:Person)-[:KNOWN_FOR]->(w:Work)
WHERE NOT EXISTS {
    MATCH (w)-[:HAS_DIRECTOR]->(p)
}
RETURN p, w

// Query with OPTIONAL MATCH

MATCH
(p:Person {birth_year: 1975})
OPTIONAL MATCH
(p)-[:KNOWN_FOR]->(w:Work)
RETURN p, w

// Query using quantified graph patterns that would be difficult to write without this functionality

MATCH (e:Episode)-[:NEXT_EPISODE*]->(e2:Episode)
RETURN e, e2

// Two different uses of WITH (e.g., to filter the results of an aggregate, to separate reading and updating the graph)

// Using WITH to filter the results of an aggregate
MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, count(w) AS workCount
WHERE workCount > 5
RETURN p, workCount

// Using WITH to separate reading and updating the graph
MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, w
WHERE w.start_year < 2000
SET p:Veteran
RETURN p, w

// Query exploring both data and graph topology

MATCH (e1:Episode)-[:NEXT_EPISODE*]->(e2:Episode)
WHERE e1.season_number = 1 AND e2.season_number = 1
RETURN e1, e2

// Query using COLLECT and UNWIND

MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, collect(w) AS works
UNWIND works AS work
RETURN p, work

// Query manipulating lists with reduce

MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WITH p, collect(w.runtime_minutes) AS runtimes
RETURN p, reduce(total = 0, runtime IN runtimes | total + runtime) AS total_runtime

// Post UNION filter with CALL

CALL {
    MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
    RETURN p, w
    UNION
    MATCH (p:Person)-[:HAS_DIRECTOR]->(w:Work)
    RETURN p, w
}
WHERE w.start_year > 2000
RETURN p, w

// Query using predicate functions like all(), any(), exists(), none(), single()

MATCH (p:Person)-[:KNOWN_FOR]->(w:Work)
WHERE all(work IN collect(w) WHERE work.start_year > 2000)
RETURN p, w