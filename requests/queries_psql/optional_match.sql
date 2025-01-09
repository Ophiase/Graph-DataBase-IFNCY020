SELECT 
    nb.id_person, nb.name, nb.birth_year, nb.death_year, nkft.id_work
FROM 
    name_basics nb
LEFT JOIN 
    name_known_for_titles nkft
ON 
    nb.id_person = nkft.id_person
WHERE 
    nb.birth_year = 1975
