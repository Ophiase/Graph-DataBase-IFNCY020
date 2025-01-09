WITH RECURSIVE episode_chain AS (
    SELECT 
        id_work, id_work_parent, season_number, episode_number, 1 AS depth
    FROM 
        work_episode
    WHERE 
        episode_number = 1
    UNION ALL
    SELECT 
        we.id_work, we.id_work_parent, we.season_number, we.episode_number, ec.depth + 1
    FROM 
        work_episode we
    INNER JOIN 
        episode_chain ec
    ON 
        we.id_work_parent = ec.id_work_parent
        AND we.season_number = ec.season_number
        AND we.episode_number = ec.episode_number + 1
    WHERE 
        ec.depth < 10
)
SELECT 
    id_work, id_work_parent, season_number, episode_number
FROM 
    episode_chain
WHERE 
    depth = 10

-- Currently it returns each node the paths
-- Return an array of node, the request is even more complexe