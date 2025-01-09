WITH RECURSIVE dijkstra AS (
    SELECT 
        id_person AS start_id, id_person AS end_id, ARRAY[id_person] AS path, 0 AS cost
    FROM 
        name_basics
    WHERE 
        name = 'James Cagney'
    UNION ALL
    SELECT 
        d.start_id, nb.id_person, d.path || nb.id_person, d.cost + nkft.weight
    FROM 
        dijkstra d
    JOIN 
        name_known_for_titles nkft ON d.end_id = nkft.id_person
    JOIN 
        name_basics nb ON nkft.id_work = nb.id_person
    WHERE 
        nb.name = 'Lauren Bacall'
)
SELECT 
    path, cost
FROM 
    dijkstra
WHERE 
    end_id = (SELECT id_person FROM name_basics WHERE name = 'Lauren Bacall')
ORDER BY 
    cost