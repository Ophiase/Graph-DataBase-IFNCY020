# I modified the original script found on the website
# Based on : https://kxs.fr/files/python/imdb_to_mysql.py

###################################################################################

import time
import os

###################################################################################

GROUP_SIZE = 1000
MAX_LINE = 40000
FOLDER = "data"

FINAL_SCRIPT_NAME = "script.sql"
FINAL_SCRIPT = """\i name_basics.sql
\i name_known_for_titles.sql
\i name_professions.sql
\i work_akas.sq
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
    print("[CREATE] work_basics.sql and work_genres.sql")
    with open(os.path.join(FOLDER, "title.basics.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_basics.sql'), 'w', encoding="utf8") as output_file, open(os.path.join(FOLDER, 'work_genres.sql'), 'w', encoding="utf8") as genre_file:
            output_file.write("DROP TABLE IF EXISTS work_basics CASCADE;\n")
            output_file.write("CREATE TABLE work_basics (id_work SERIAL PRIMARY KEY, worktype VARCHAR(50), primary_title VARCHAR(1000), original_title VARCHAR(1000), is_adult SMALLINT, start_year SMALLINT, end_year SMALLINT, runtime_minutes INTEGER);\n")
            genre_file.write("DROP TABLE IF EXISTS work_genres CASCADE;\n")
            genre_file.write(
                "CREATE TABLE work_genres (id_work INTEGER, genre VARCHAR(50), PRIMARY KEY (id_work, genre));\n")
            file.readline()
            nb = 0
            nb_genre = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO work_basics VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                tabLine[0] = tabLine[0][2:].lstrip("0")
                for i in (1, 2, 3, 8):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (4, 5, 6, 7):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                if tabLine[8] != "NULL":
                    genres = tabLine[8][1:-1].split(",")
                    for genre in genres:
                        nb_genre += 1
                        if nb_genre % group_size == 1:
                            genre_file.write("INSERT INTO work_genres VALUES ")
                        values = "({}, '{}')".format(tabLine[0], genre)
                        if nb_genre % group_size == 0:
                            genre_file.write(", " + values + ";\n")
                        elif nb_genre % group_size == 1:
                            genre_file.write(values)
                        else:
                            genre_file.write(", " + values)
                tabLine = tabLine[:-1]
                values = "({}, {}, {}, {}, {}, {}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_genre % group_size != 0:
                genre_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_worktype;\n")
            output_file.write(
                "CREATE INDEX IX_worktype ON work_basics (worktype);\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_original_title;\n")
            output_file.write(
                "CREATE INDEX IX_original_title ON work_basics (original_title);\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_start_year;\n")
            output_file.write(
                "CREATE INDEX IX_start_year ON work_basics (start_year);\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_runtime_minutes;\n")
            output_file.write(
                "CREATE INDEX IX_runtime_minutes ON work_basics (runtime_minutes);\n")
            genre_file.write(
                "DROP INDEX IF EXISTS IX_id_work;\n")
            genre_file.write(
                "CREATE INDEX IX_id_work ON work_genres (id_work);\n")
            genre_file.write("DROP INDEX IF EXISTS IX_genre;\n")
            genre_file.write("CREATE INDEX IX_genre ON work_genres (genre);\n")
            print("File work_basics.sql created")
            print("File work_genres.sql created")


def generate_work_principals(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] work_principals.sql")
    with open(os.path.join(FOLDER, "title.principals.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_principals.sql'), 'w', encoding="utf8") as output_file:
            output_file.write(
                "DROP TABLE IF EXISTS work_principals CASCADE;\n")
            output_file.write(
                "CREATE TABLE IF NOT EXISTS work_principals (id_work INTEGER, ordering SMALLINT, id_person INTEGER, category VARCHAR(50), job VARCHAR(500), characters VARCHAR(1400), PRIMARY KEY (id_work, ordering));\n")
            file.readline()
            nb = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO work_principals VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                for i in range(3, len(tabLine)):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[2] = tabLine[2][2:].lstrip("0")
                values = "({}, {}, {}, {}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_person;\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_principals (id_person);\n")
            print("File work_principals.sql created")


def generate_work_akas(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] work_akas.sql and work_types.sql")
    with open(os.path.join(FOLDER, "title.akas.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_akas.sql'), 'w', encoding="utf8") as output_file, open(os.path.join(FOLDER, 'work_types.sql'), 'w', encoding="utf8") as types_file:
            output_file.write("DROP TABLE IF EXISTS work_akas CASCADE;\n")
            output_file.write("CREATE TABLE work_akas (id_work INTEGER, ordering SMALLINT, title VARCHAR(1000), region VARCHAR(4), language VARCHAR(3), attributes VARCHAR(200), is_original_title SMALLINT, PRIMARY KEY (id_work, ordering));\n")
            types_file.write("DROP TABLE IF EXISTS work_types CASCADE;\n")
            types_file.write("CREATE TABLE work_types (id_work INTEGER, ordering SMALLINT, type VARCHAR(50) CHECK (type IN ('alternative', 'dvd', 'festival', 'tv', 'video', 'working', 'original', 'imdbDisplay')), PRIMARY KEY (id_work, ordering));\n")
            file.readline()
            nb = 0
            nb_typ = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO work_akas VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                tabLine[0] = tabLine[0][2:].lstrip("0")
                for i in (2, 3, 4, 5, 6):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (1, 7):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                tabLine[5] = tabLine[5].replace("\x02", ",")
                if tabLine[5] != "NULL":
                    types = tabLine[5][1:-1].split(",")
                    for typ in types:
                        nb_typ += 1
                        if nb_typ % group_size == 1:
                            types_file.write("INSERT INTO work_types VALUES ")
                        values = "({}, {}, '{}')".format(
                            tabLine[0], tabLine[1], typ)
                        if nb_typ % group_size == 0:
                            types_file.write(", " + values + ";\n")
                        elif nb_typ % group_size == 1:
                            types_file.write(values)
                        else:
                            types_file.write(", " + values)
                tabLine.pop(5)
                values = "({}, {}, {}, {}, {}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_typ % group_size != 0:
                types_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_work_ordering;\n")
            output_file.write(
                "CREATE INDEX IX_id_work_ordering ON work_akas (id_work, ordering);\n")
            types_file.write(
                "DROP INDEX IF EXISTS IX_id_work_ordering;\n")
            types_file.write(
                "CREATE INDEX IX_id_work_ordering ON work_types (id_work, ordering);\n")
            print("File work_akas.sql created")
            print("File work_types.sql created")


def generate_work_ratings(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] work_ratings.sql")
    with open(os.path.join(FOLDER, "title.ratings.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_ratings.sql'), 'w', encoding="utf8") as output_file:
            output_file.write("DROP TABLE IF EXISTS work_ratings CASCADE;\n")
            output_file.write(
                "CREATE TABLE work_ratings (id_work INTEGER PRIMARY KEY, average_rating DECIMAL(3,1), num_votes INTEGER);\n")
            file.readline()
            nb = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO work_ratings VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                tabLine[0] = tabLine[0][2:].lstrip("0")
                for i in (1, 2):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                values = "({}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            print("File work_ratings.sql created")


def generate_work_episode(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] work_episode.sql")
    with open(os.path.join(FOLDER, "title.episode.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_episode.sql'), 'w', encoding="utf8") as output_file:
            output_file.write("DROP TABLE IF EXISTS work_episode CASCADE;\n")
            output_file.write(
                "CREATE TABLE work_episode (id_work INTEGER PRIMARY KEY, id_work_parent INTEGER, season_number SMALLINT, episode_number INTEGER);\n")
            file.readline()
            nb = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO work_episode VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[1] = tabLine[1][2:].lstrip("0")
                for i in range(2, len(tabLine)):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                values = "({}, {}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_work_parent;\n")
            output_file.write(
                "CREATE INDEX IX_id_work_parent ON work_episode (id_work_parent);\n")
            print("File work_episode.sql created")


def generate_name_basics(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] name_basics.sql, name_professions.sql and name_known_for_titles.sql")
    with open(os.path.join(FOLDER, "name.basics.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'name_basics.sql'), 'w', encoding="utf8") as output_file, open(os.path.join(FOLDER, 'name_professions.sql'), 'w', encoding="utf8") as profession_file, open(os.path.join(FOLDER, 'name_known_for_titles.sql'), 'w', encoding="utf8") as known_file:
            output_file.write("DROP TABLE IF EXISTS name_basics CASCADE;\n")
            output_file.write(
                "CREATE TABLE name_basics (id_person INTEGER PRIMARY KEY, name VARCHAR(200), birth_year SMALLINT, death_year SMALLINT);\n")
            profession_file.write(
                "DROP TABLE IF EXISTS name_professions CASCADE;\n")
            profession_file.write(
                "CREATE TABLE name_professions (id_person INTEGER, profession VARCHAR(50), PRIMARY KEY (id_person, profession));\n")
            known_file.write(
                "DROP TABLE IF EXISTS name_known_for_titles CASCADE;\n")
            known_file.write(
                "CREATE TABLE name_known_for_titles (id_person INTEGER, id_work INTEGER, PRIMARY KEY (id_person, id_work));\n")
            file.readline()
            nb = 0
            nb_prof = 0
            nb_known = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                if nb % group_size == 1:
                    output_file.write("INSERT INTO name_basics VALUES ")
                cleanLine = line[:-1]
                tabLine = cleanLine.split("\t")
                tabLine[0] = tabLine[0][2:].lstrip("0")
                for i in (1, 4, 5):
                    if tabLine[i] == "\\N" or tabLine[i] == '':
                        tabLine[i] = "NULL"
                    else:
                        tabLine[i] = "'" + \
                            tabLine[i].replace("'", "''").replace(
                                "\\", "\\\\") + "'"
                for i in (2, 3):
                    if tabLine[i] == "\\N":
                        tabLine[i] = "NULL"
                if tabLine[4] != "NULL":
                    profs = tabLine[4][1:-1].split(",")
                    for prof in profs:
                        nb_prof += 1
                        if nb_prof % group_size == 1:
                            profession_file.write(
                                "INSERT INTO name_professions VALUES ")
                        values = "({}, '{}')".format(tabLine[0], prof)
                        if nb_prof % group_size == 0:
                            profession_file.write(", " + values + ";\n")
                        elif nb_prof % group_size == 1:
                            profession_file.write(values)
                        else:
                            profession_file.write(", " + values)
                if tabLine[5] != "NULL":
                    known_ids = tabLine[5][1:-1].split(",")
                    for known_id in known_ids:
                        nb_known += 1
                        known_id = known_id[2:].lstrip("0")
                        if nb_known % group_size == 1:
                            known_file.write(
                                "INSERT INTO name_known_for_titles VALUES ")
                        values = "({}, {})".format(tabLine[0], known_id)
                        if nb_known % group_size == 0:
                            known_file.write(", " + values + ";\n")
                        elif nb_known % group_size == 1:
                            known_file.write(values)
                        else:
                            known_file.write(", " + values)
                tabLine = tabLine[:-2]
                values = "({}, {}, {}, {})".format(*tabLine)
                if nb % group_size == 0:
                    output_file.write(", " + values + ";\n")
                elif nb % group_size == 1:
                    output_file.write(values)
                else:
                    output_file.write(", " + values)
            if nb % group_size != 0:
                output_file.write(";\n")
            if nb_prof % group_size != 0:
                profession_file.write(";\n")
            if nb_known % group_size != 0:
                known_file.write(";\n")
            output_file.write("CREATE INDEX IX_name ON name_basics (name);\n")
            profession_file.write(
                "DROP INDEX IF EXISTS IX_id_person;\n")
            profession_file.write(
                "CREATE INDEX IX_id_person ON name_professions (id_person);\n")
            profession_file.write(
                "DROP INDEX IF EXISTS IX_profession;\n")
            profession_file.write(
                "CREATE INDEX IX_profession ON name_professions (profession);\n")
            known_file.write(
                "DROP INDEX IF EXISTS IX_id_person;\n")
            known_file.write(
                "CREATE INDEX IX_id_person ON name_known_for_titles (id_person);\n")
            known_file.write(
                "DROP INDEX IF EXISTS IX_id_work;\n")
            known_file.write(
                "CREATE INDEX IX_id_work ON name_known_for_titles (id_work);\n")
            print("File name_basics.sql created")
            print("File name_professions.sql created")
            print("File name_known_for_titles.sql created")


def generate_title_crew(group_size: int = GROUP_SIZE, max_line: int = MAX_LINE):
    print("[CREATE] work_director.sql and work_writer.sql")
    with open(os.path.join(FOLDER, "title.crew.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_director.sql'), 'w', encoding="utf8") as output_file:
            output_file.write("DROP TABLE IF EXISTS work_director CASCADE;\n")
            output_file.write(
                "CREATE TABLE work_director (id_work INTEGER, id_person INTEGER, PRIMARY KEY (id_work, id_person));\n")
            file.readline()
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                clean_line = line[:-1]
                tab_line = clean_line.split("\t")
                tab_line[0] = tab_line[0][2:].lstrip("0")
                for i in range(1, len(tab_line)):
                    if tab_line[i] == "\\N":
                        tab_line[i] = "NULL"
                if tab_line[1] != "NULL":
                    directors = tab_line[1].split(",")
                    for director in directors:
                        nb_insert += 1
                        if nb_insert % group_size == 1:
                            output_file.write(
                                "INSERT INTO work_director VALUES ")
                        values = "({}, {})".format(
                            tab_line[0], director[2:].lstrip("0"))
                        if nb_insert % group_size == 0:
                            output_file.write(", " + values + ";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values)
                        else:
                            output_file.write(", " + values)
            if nb_insert % group_size != 0:
                output_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_work;\n")
            output_file.write(
                "CREATE INDEX IX_id_work ON work_director (id_work);\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_person;\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_director (id_person);\n")
            print("File work_director.sql created")
    with open(os.path.join(FOLDER, "title.crew.tsv"), 'r', encoding="utf8") as file:
        with open(os.path.join(FOLDER, 'work_writer.sql'), 'w', encoding="utf8") as output_file:
            output_file.write("DROP TABLE IF EXISTS work_writer CASCADE;\n")
            output_file.write(
                "CREATE TABLE work_writer (id_work INTEGER, id_person INTEGER, PRIMARY KEY (id_work, id_person));\n")
            file.readline()
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            for line in file:
                if max_line is not None and nb == max_line:
                    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    print(nb, "line processed:", round(fin - debut), "seconds")
                clean_line = line[:-1]
                tab_line = clean_line.split("\t")
                tab_line[0] = tab_line[0][2:].lstrip("0")
                for i in range(1, len(tab_line)):
                    if tab_line[i] == "\\N":
                        tab_line[i] = "NULL"
                if tab_line[2] != "NULL":
                    writers = tab_line[2].split(",")
                    for writer in writers:
                        nb_insert += 1
                        if nb_insert % group_size == 1:
                            output_file.write(
                                "INSERT INTO work_writer VALUES ")
                        values = "({}, {})".format(
                            tab_line[0], writer[2:].lstrip("0"))
                        if nb_insert % group_size == 0:
                            output_file.write(", " + values + ";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values)
                        else:
                            output_file.write(", " + values)
            if nb_insert % group_size != 0:
                output_file.write(";\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_work;\n")
            output_file.write(
                "CREATE INDEX IX_id_work ON work_writer (id_work);\n")
            output_file.write(
                "DROP INDEX IF EXISTS IX_id_person;\n")
            output_file.write(
                "CREATE INDEX IX_id_person ON work_writer (id_person);\n")
            print("File work_writer.sql created")


def generate_script() -> None:
    print("[CREATE] script.sql")
    with open(os.path.join(FOLDER, FINAL_SCRIPT_NAME), 'w') as file:
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
