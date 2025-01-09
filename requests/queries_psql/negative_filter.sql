SELECT 
    nkft.id_person, nkft.id_work
FROM 
    name_known_for_titles nkft
LEFT JOIN 
    work_director wd
ON 
    nkft.id_person = wd.id_person AND nkft.id_work = wd.id_work
WHERE 
    wd.id_person IS NULL
