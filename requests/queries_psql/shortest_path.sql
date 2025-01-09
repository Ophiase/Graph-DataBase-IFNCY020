WITH RECURSIVE shortest_path AS (
    SELECT 
        id_person AS start_id, id_person AS end_id, ARRAY[id_person] AS path, 0 AS depth
    FROM 
        name_basics
    WHERE 
        name = 'James Cagney'
    UNION ALL
    SELECT 
        sp.start_id, nb.id_person, sp.path || nb.id_person, sp.depth + 1
    FROM 
        shortest_path sp
    JOIN 
        name_known_for_titles nkft ON sp.end_id = nkft.id_person
    JOIN 
        name_basics nb ON nkft.id_work = -- ERROR, I have to rethink this part
    WHERE 
        nb.name = 'Lauren Bacall'
)
SELECT 
    path
FROM 
    shortest_path
WHERE 
    end_id = (SELECT id_person FROM name_basics WHERE name = 'Lauren Bacall')
ORDER BY 
    depth
