# I modified the original script found on the website

###################################################################################

import time
import os

###################################################################################

GROUP_SIZE = 1000
MAX_LINE = 100000
FOLDER = "data"

FINAL_SCRIPT_NAME = "script.sql"
FINAL_SCRIPT = """\i name_basics.sql
\i name_knownForTitles.sql
\i name_professions.sql
\i work_akas.sql
\i work_basics.sql
\i work_director.sql
\i work_episode.sql
\i work_genres.sql
\i work_principals.sql
\i work_ratings.sql
\i work_types.sql
\i work_writer.sql"""

###################################################################################


def generate_work_basics(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_basics.sql and work_genres.sql")
    with open(FOLDER + "/" + "title.basics.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_basics.sql', 'w', encoding="utf8") as output_file, open(FOLDER + "/" + 'work_genres.sql', 'w', encoding="utf8") as genre_file:

            output_file.write("DROP TABLE IF EXISTS \"work_basics\";\n")

            output_file.write("CREATE TABLE \"work_basics\" (id_work SERIAL PRIMARY KEY, worktype VARCHAR(50), primaryTitle VARCHAR(1000), originalTitle VARCHAR(1000), isAdult SMALLINT, startYear SMALLINT, endYear SMALLINT, runtimeMinutes INTEGER);\n")

            genre_file.write("DROP TABLE IF EXISTS \"work_genres\";\n")

            genre_file.write("CREATE TABLE \"work_genres\" (id_work INTEGER, genre VARCHAR(50), PRIMARY KEY (id_work, genre));\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            nb_genre = 0
            # cat = set()
            # genreList = set()
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"work_basics\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (1, 2, 3, 8):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # On ajoute and on échappe les quotes (et les antislash)
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (4, 5, 6, 7):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                # cat.add(tabLine[1])

                # On s'occupe des genres
                if tabLine[8] != "NULL":
                    genres = tabLine[8][1:-1].split(",")
                    for genre in genres:
                        nb_genre += 1
                        if nb_genre % group_size == 1:
                            genre_file.write(
                                "INSERT INTO \"work_genres\" VALUES ")
                        values = "({}, {})"
                        if nb_genre % group_size == 0:
                            genre_file.write(
                                ", " + values.format(tabLine[0], "'" + genre + "'")+";\n")
                        elif nb_genre % group_size == 1:
                            genre_file.write(values.format(
                                tabLine[0], "'" + genre + "'"))
                        else:
                            genre_file.write(
                                ", " + values.format(tabLine[0], "'" + genre + "'"))

                        # genreList.add(genre)

                # On insère la ligne avec le genre en moins
                tabLine = tabLine[:-1]
                values = "({}, {}, {}, {}, {}, {}, {}, {})"
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_genre % group_size != 0:
                genre_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "ALTER TABLE work_basics ADD PRIMARY KEY (id_work);\n")
            output_file.write(
                "CREATE INDEX IX_worktype ON work_basics (worktype);\n")
            output_file.write(
                "CREATE INDEX IX_originalTitle ON work_basics (originalTitle);\n")
            output_file.write(
                "CREATE INDEX IX_startYear ON work_basics (startYear);\n")
            output_file.write(
                "CREATE INDEX IX_runtimeMinutes ON work_basics (runtimeMinutes);\n")
            print("File work_basics.sql created")
            genre_file.write(
                "CREATE INDEX IX_id_work ON work_genres (id_work);\n")
            genre_file.write("CREATE INDEX IX_genre ON work_genres (genre);\n")
            print("File work_genres.sql created")
            # print(cat)
            # print(genreList)
            print()


def generate_work_principals(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_principals.sql")
    with open(FOLDER + "/" + "title.principals.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_principals.sql', 'w', encoding="utf8") as output_file:

            output_file.write("DROP TABLE IF EXISTS \"work_principals\";\n")

            output_file.write("CREATE TABLE IF NOT EXISTS \"work_principals\" (id_work INTEGER, ordering SMALLINT, id_person INTEGER, category VARCHAR(50), job VARCHAR(500), characters VARCHAR(1400), PRIMARY KEY (id_work, ordering));\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            # cat = set()
            # max_size = 0
            nb = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"work_principals\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # Nettoyage des champs
                for i in range(3, len(tabLine)):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # On ajoute and on échappe les quotes (et les antislash)
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                # cat.add(tabLine[3])
                # if len(tabLine[5]) > max_size:
                #   max_size = len(tabLine[5])
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[2] = tabLine[2][2:].lstrip("0")

                # On insère la ligne
                values = "({}, {}, {}, {}, {}, {})"
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "CREATE UNIQUE INDEX UX_id_work_ordering ON work_principals (id_work, ordering);\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_principals (id_person);\n")

            print("File work_principals.sql created")
            # print(cat)
            # print(max_size)
            print()


def generate_work_akas(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_akas.sql and work_types.sql")
    with open(FOLDER + "/" + "title.akas.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_akas.sql', 'w', encoding="utf8") as output_file, open(FOLDER + "/" + 'work_types.sql', 'w', encoding="utf8") as types_file:

            output_file.write("DROP TABLE IF EXISTS \"work_akas\";\n")

            output_file.write(
                "CREATE TABLE \"work_akas\" ("
                "id_work INTEGER, "
                "ordering SMALLINT, "
                "title VARCHAR(1000), "
                "region VARCHAR(4), "
                "language VARCHAR(3), "
                "attributes VARCHAR(200), "
                "isOriginalTitle SMALLINT, "
                "PRIMARY KEY (id_work, ordering)"
                ");\n"
            )

            types_file.write("DROP TABLE IF EXISTS \"work_types\";\n")

            types_file.write(
                "CREATE TABLE \"work_types\" ("
                "id_work INTEGER, "
                "ordering SMALLINT, "
                "type VARCHAR(50) CHECK (type IN ('alternative', 'dvd', 'festival', 'tv', 'video', 'working', 'original', 'imdbDisplay')), "
                "PRIMARY KEY (id_work, ordering)"
                ");\n"
            )
            
            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            nb_typ = 0
            # cat = set()
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"work_akas\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (2, 3, 4, 5, 6):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # On ajoute and on échappe les quotes (et les antislash)
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (1, 7):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                # On enlève le séparateur bizarre de l'imdb and on le remplace par une virgule
                tabLine[5] = tabLine[5].replace("\x02", ",")
                # cat.add(tabLine[5])

                # On s'occupe des types
                if tabLine[5] != "NULL":
                    types = tabLine[5][1:-1].split(",")
                    for typ in types:
                        nb_typ += 1
                        if nb_typ % group_size == 1:
                            types_file.write(
                                "INSERT INTO \"work_types\" VALUES ")
                        values = "({}, {}, {})"
                        if nb_typ % group_size == 0:
                            types_file.write(
                                ", " + values.format(tabLine[0], tabLine[1], "'" + typ + "'")+";\n")
                        elif nb_typ % group_size == 1:
                            types_file.write(values.format(
                                tabLine[0], tabLine[1], "'" + typ + "'"))
                        else:
                            types_file.write(
                                ", " + values.format(tabLine[0], tabLine[1], "'" + typ + "'"))

                # On insère la ligne sans le type
                tabLine.pop(5)
                values = "({}, {}, {}, {}, {}, {}, {})"
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_typ % group_size != 0:
                types_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "CREATE UNIQUE INDEX UX_id_work_ordering ON work_akas (id_work, ordering);\n")
            print("File work_akas.sql created")
            types_file.write(
                "CREATE INDEX IX_id_work_ordering ON work_types (id_work, ordering);\n")
            print("File work_types.sql created")
            # print(cat)
            print()


def generate_work_ratings(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_ratings.sql")
    with open(FOLDER + "/" + "title.ratings.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_ratings.sql', 'w', encoding="utf8") as output_file:

            output_file.write("DROP TABLE IF EXISTS \"work_ratings\";\n")

            output_file.write(
                "CREATE TABLE \"work_ratings\" (id_work INTEGER PRIMARY KEY, averageRating DECIMAL(3,1), numVotes INTEGER);\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            debut = time.perf_counter()
            values = "({}, {}, {})"
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"work_ratings\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (1, 2):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # else: # On ajoute and on échappe les quotes
                        # tabLine[i] = "'"+ tabLine[i].replace("'", "''") + "'"

                # On insère la ligne
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "ALTER TABLE work_ratings ADD PRIMARY KEY (id_work);\n")
            print("File work_ratings.sql created")
            print()


def generate_work_episode(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_episode.sql")
    with open(FOLDER + "/" + "title.episode.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_episode.sql', 'w', encoding="utf8") as output_file:

            output_file.write("DROP TABLE IF EXISTS \"work_episode\";\n")

            output_file.write(
                "CREATE TABLE \"work_episode\" ("
                "id_work INTEGER PRIMARY KEY, "
                "id_work_parent INTEGER, "
                "seasonNumber SMALLINT, "
                "episodeNumber INTEGER"
                ");\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            debut = time.perf_counter()
            # maxi = 0
            # Une accolade par champ
            values = "({}, {}, {}, {})"
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"work_episode\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[1] = tabLine[1][2:].lstrip("0")
                # Nettoyage des champs (en évitant ceux qui sont des id si on peut)
                for i in range(2, len(tabLine)):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # else: # On ajoute and on échappe les quotes
                        # tabLine[i] = "'"+ tabLine[i].replace("'", "''") + "'"

                # if tabLine[i] != "NULL" and int(tabLine[3]) > maxi:
                #    maxi = int(tabLine[3])
                # On insère la ligne
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "ALTER TABLE work_episode ADD PRIMARY KEY (id_work);\n")
            output_file.write(
                "CREATE INDEX IX_id_work_parent ON work_episode (id_work_parent);\n")
            print("File work_episode.sql created")
            # print(maxi)
            print()


def generate_name_basics(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  name_basics.sql, name_professions.sql and name_knownForTitles.sql")
    with open(FOLDER + "/" + "name.basics.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'name_basics.sql', 'w', encoding="utf8") as output_file, open(FOLDER + "/" + 'name_professions.sql', 'w', encoding="utf8") as profession_file, open(FOLDER + "/" + 'name_knownForTitles.sql', 'w', encoding="utf8") as known_file:
            output_file.write("DROP TABLE IF EXISTS name_basics;\n")

            output_file.write(
                "CREATE TABLE name_basics (id_person INTEGER PRIMARY KEY, name VARCHAR(200), birthYear SMALLINT, deathYear SMALLINT);\n")

            # Professions

            profession_file.write("DROP TABLE IF EXISTS name_professions;\n")

            profession_file.write("CREATE TABLE name_professions (id_person INTEGER, profession VARCHAR(50), PRIMARY KEY (id_person, profession));\n")

            # knownForTitles

            known_file.write("DROP TABLE IF EXISTS name_knownForTitles;\n")

            known_file.write(
                "CREATE TABLE name_knownForTitles (id_person INTEGER, id_work INTEGER, PRIMARY KEY (id_person, id_work));\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            nb_prof = 0
            nb_known = 0
            debut = time.perf_counter()
            # maxi = 0
            # profList = set()

            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                if nb % group_size == 1:
                    output_file.write("INSERT INTO \"name_basics\" VALUES ")
                # On enlève le retour chariot
                cleanLine = line[:-1]

                tabLine = cleanLine.split("\t")
                # On enlève les deux lettres au début des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs (en évitant ceux qui sont des id si on peut simplement)
                for i in (1, 4, 5):
                    if tabLine[i] == "\\N" or tabLine[i] == '':  # On ajoute NULL
                        tabLine[i] = "NULL"
                    # On ajoute and on échappe les quotes (et les antislash)
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (2, 3):
                    if tabLine[i] == "\\N":  # On ajoute NULL
                        tabLine[i] = "NULL"
                # if len(tabLine[5]) > maxi:
                #    maxi = len(tabLine[5])

                # On extrait toutes les professions
                if tabLine[4] != "NULL":
                    profs = tabLine[4][1:-1].split(",")
                    for prof in profs:
                        nb_prof += 1
                        if nb_prof % group_size == 1:
                            profession_file.write(
                                "INSERT INTO \"name_professions\" VALUES ")
                        values = "({}, {})"
                        if nb_prof % group_size == 0:
                            profession_file.write(
                                ", " + values.format(tabLine[0], "'" + prof + "'")+";\n")
                        elif nb_prof % group_size == 1:
                            profession_file.write(values.format(
                                tabLine[0], "'" + prof + "'"))
                        else:
                            profession_file.write(
                                ", " + values.format(tabLine[0], "'" + prof + "'"))
                        # profList.add(prof)

                # On extrait les knownForTitles
                if tabLine[5] != "NULL":
                    # On récupère les ids avec tt and les 0
                    known_ids = tabLine[5][1:-1].split(",")
                    for known_id in known_ids:
                        nb_known += 1
                        # On extrait l'id
                        known_id = known_id[2:].lstrip("0")
                        if nb_known % group_size == 1:
                            known_file.write(
                                "INSERT INTO \"name_knownForTitles\" VALUES ")
                        values = "({}, {})"
                        if nb_known % group_size == 0:
                            known_file.write(
                                ", " + values.format(tabLine[0], known_id)+";\n")
                        elif nb_known % group_size == 1:
                            known_file.write(
                                values.format(tabLine[0], known_id))
                        else:
                            known_file.write(
                                ", " + values.format(tabLine[0], known_id))

                # On insère la ligne sans professio and knownForTitles
                # Une accolade par champ
                tabLine = tabLine[:-2]
                values = "({}, {}, {}, {})"
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_prof % group_size != 0:
                profession_file.write(";\n")
            if nb_known % group_size != 0:
                known_file.write(";\n")

            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "ALTER TABLE name_basics ADD PRIMARY KEY (id_person);\n")
            # Pour les recherches sur les noms
            output_file.write("CREATE INDEX IX_name ON name_basics (name);\n")
            print("File name_basics.sql created")
            profession_file.write(
                "CREATE INDEX IX_id_person ON name_professions (id_person);\n")
            profession_file.write(
                "CREATE INDEX IX_profession ON name_professions (profession);\n")
            print("File name_professions.sql created")
            known_file.write(
                "CREATE INDEX IX_id_person ON name_knownForTitles (id_person);\n")
            known_file.write(
                "CREATE INDEX IX_id_work ON name_knownForTitles (id_work);\n")
            print("File name_knownForTitles.sql created")
            print()

            # print(maxi)
            # print(profList)


def generate_title_crew(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE]  work_director.sql and work_writer.sql")
    # On fait deux passages pour simplifier

    # Directors
    with open(FOLDER + "/" + "title.crew.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_director.sql', 'w', encoding="utf8") as output_file:

            output_file.write("DROP TABLE IF EXISTS \"work_director\";\n")

            output_file.write(
                "CREATE TABLE \"work_director\" (id_work INTEGER, id_person INTEGER, PRIMARY KEY (id_work, id_person));\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            # Une accolade par champ
            values = "({}, {})"
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                # On enlève le retour chariot
                clean_line = line[:-1]

                tab_line = clean_line.split("\t")
                # On enlève les deux lettres au début des identifiants
                tab_line[0] = tab_line[0][2:].lstrip("0")
                # Nettoyage des champs (en évitant ceux qui sont des id si on peut simplement)
                for i in range(1, len(tab_line)):
                    if tab_line[i] == "\\N":  # On ajoute NULL
                        tab_line[i] = "NULL"

                if tab_line[1] != "NULL":
                    directors = tab_line[1].split(",")
                    # print(directors)
                    for director in directors:
                        nb_insert = nb_insert + 1
                        if nb_insert % group_size == 1:
                            output_file.write(
                                "INSERT INTO \"work_director\" VALUES ")
                        # On insère la ligne
                        if nb_insert % group_size == 0:
                            output_file.write(
                                ", " + values.format(tab_line[0], director[2:].lstrip("0"))+";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values.format(
                                tab_line[0], director[2:].lstrip("0")))
                        else:
                            output_file.write(
                                ", " + values.format(tab_line[0], director[2:].lstrip("0")))

            # Si nous n'avons pas fini un groupe
            if nb_insert % group_size != 0:
                output_file.write(";\n")
            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "CREATE INDEX IX_id_work ON work_director (id_work);\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_director (id_person);\n")
            print("File work_director.sql created")
            print()

    # Writers
    with open(FOLDER + "/" + "title.crew.tsv", 'r', encoding="utf8") as file:
        with open(FOLDER + "/" + 'work_writer.sql', 'w', encoding="utf8") as output_file:

            output_file.write("DROP TABLE IF EXISTS \"work_writer\";\n")

            output_file.write(
                "CREATE TABLE \"work_writer\" (id_work INTEGER, id_person INTEGER, PRIMARY KEY (id_work, id_person));\n")

            # On évacue la première ligne avec le nom des champs
            file.readline()

            # On parcourt toutes les lignes
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            # Une accolade par champ
            values = "({}, {})"
            for line in file:
                if max_line is not None and nb == max_line:
                    break

                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "line processed:", temps, "seconds")

                # On enlève le retour chariot
                clean_line = line[:-1]
                # print(line)

                tab_line = clean_line.split("\t")
                # On enlève les deux lettres au début des identifiants
                tab_line[0] = tab_line[0][2:].lstrip("0")
                # Nettoyage des champs (en évitant ceux qui sont des id si on peut simplement)
                for i in range(1, len(tab_line)):
                    if tab_line[i] == "\\N":  # On ajoute NULL
                        tab_line[i] = "NULL"

                if tab_line[2] != "NULL":
                    writers = tab_line[2].split(",")
                    # print(directors)
                    for writer in writers:
                        nb_insert = nb_insert + 1
                        if nb_insert % group_size == 1:
                            output_file.write(
                                "INSERT INTO \"work_writer\" VALUES ")
                        # On insère la ligne
                        if nb_insert % group_size == 0:
                            output_file.write(
                                ", " + values.format(tab_line[0], writer[2:].lstrip("0"))+";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values.format(
                                tab_line[0], writer[2:].lstrip("0")))
                        else:
                            output_file.write(
                                ", " + values.format(tab_line[0], writer[2:].lstrip("0")))

            # Si nous n'avons pas fini un groupe
            if nb_insert % group_size != 0:
                output_file.write(";\n")
            # Création des index pour avoir des requêtes plus performantes
            output_file.write(
                "CREATE INDEX IX_id_work ON work_writer (id_work);\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_writer (id_person);\n")
            print("File work_writer.sql created")
            print()

def generate_script() -> None:
    print("[CREATE] script.sql")
    with open(os.path.join(FOLDER, FINAL_SCRIPT_NAME), 'w') as file :
        file.write(FINAL_SCRIPT)

###################################################################################

def main() -> None:
    generate_work_basics()
    generate_work_principals()
    generate_work_akas()
    generate_work_ratings()
    generate_work_episode()
    generate_name_basics()
    generate_title_crew()
    generate_script()

if __name__ == "__main__":
    main()