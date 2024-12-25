# This is the original script I found on the website

# v1.1
# Ajout des nouvelles catÃ©gories dans work_principals
# Ajout des nouvelles professions dans name_profession


import time

# Origine des fichiers :
# https://datasets.imdbws.com/
# Documentation :
# https://www.imdb.com/interfaces/


# Changements de noms d'attributs pour des raisons pÃ©dagogiques :
# tconst -> id_work
# nconst -> id_person
# primaryName -> name


# title.basics.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# tconst (string) - alphanumeric unique identifier of the title
# titleType (string) â€“ the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
# primaryTitle (string) â€“ the more popular title / the title used by the filmmakers on promotional materials at the point of release
# originalTitle (string) - original title, in the original language
# isAdult (boolean) - 0: non-adult title; 1: adult title
# startYear (YYYY) â€“ represents the release year of a title. In the case of TV Series, it is the series start year
# endYear (YYYY) â€“ TV Series end year. â€˜\Nâ€™ for all other title types
# runtimeMinutes â€“ primary runtime of the title, in minutes
# genres (string array) â€“ includes up to three genres associated with the title
#
#
# Choix pour la base MySQLÂ :
# 
# table work_basicsÂ :
# id_work : unsigned int
# worktype : ENUM('tvEpisode', 'tvMiniSeries', 'short', 'tvMovie', 'tvSeries', 'tvShort', 'video', 'videoGame', 'movie', 'tvSpecial')
# primaryTitle : varchar(1000)
# originalTitle : varchar(1000)
# isAdult : tinyint
# startYear : smallint
# endYear : smallint
# runtimeMinutes : unsigned mediumint
#
# table work_genresÂ :
# id_work : unsigned int
# genreÂ : ENUM('Romance', 'Talk-Show', 'Drama', 'Fantasy', 'Action', 'Sci-Fi', 'Animation', 'Thriller', 'Comedy', 'Documentary', 'Reality-TV', 'Adventure', 'Mystery', 'Film-Noir', 'Game-Show', 'Horror', 'Music', 'Family', 'Adult', 'Sport', 'War', 'Biography', 'History', 'Crime', 'News', 'Western', 'Musical', 'Short')

def generateWorkBasics(group_size = 1000):
    print("CrÃ©ation de work_basics.sql et work_genres.sql")
    with open("title.basics.tsv", 'r', encoding="utf8") as file:
        with open('work_basics.sql', 'w', encoding="utf8") as output_file, open('work_genres.sql', 'w', encoding="utf8") as genre_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_basics`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_basics` (id_work INT UNSIGNED, worktype ENUM('tvEpisode', 'tvMiniSeries', 'short', 'tvMovie', 'tvSeries', 'tvShort', 'video', 'videoGame', 'movie', 'tvSpecial', 'tvPilot'), primaryTitle VARCHAR(1000), originalTitle VARCHAR(1000), isAdult TINYINT, startYear SMALLINT, endYear SMALLINT, runtimeMinutes MEDIUMINT UNSIGNED);\n")
            
            # Suppression de la table
            genre_file.write("DROP TABLE IF EXISTS `work_genres`;\n")
            # CrÃ©ation de la table
            genre_file.write("CREATE TABLE `work_genres` (id_work INT UNSIGNED, genre ENUM('Romance', 'Talk-Show', 'Drama', 'Fantasy', 'Action', 'Sci-Fi', 'Animation', 'Thriller', 'Comedy', 'Documentary', 'Reality-TV', 'Adventure', 'Mystery', 'Film-Noir', 'Game-Show', 'Horror', 'Music', 'Family', 'Adult', 'Sport', 'War', 'Biography', 'History', 'Crime', 'News', 'Western', 'Musical', 'Short'));\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            nb_genre = 0
            #cat = set()
            #genreList = set()
            debut = time.perf_counter()
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `work_basics` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (1, 2, 3, 8):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                    else: # On ajoute et on Ã©chappe les quotes (et les antislash)
                        tabLine[i] = "'"+ tabLine[i].replace("'", "''").replace("\\", "\\\\") + "'"
                for i in (4, 5, 6, 7):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                #cat.add(tabLine[1])
                
                # On s'occupe des genres
                if tabLine[8] != "NULL":
                    genres = tabLine[8][1:-1].split(",")
                    for genre in genres:
                        nb_genre += 1
                        if nb_genre % group_size == 1:
                            genre_file.write("INSERT INTO `work_genres` VALUES ")
                        values = "({}, {})"
                        if nb_genre % group_size == 0:
                            genre_file.write(", " + values.format(tabLine[0], "'" + genre + "'")+";\n")
                        elif nb_genre % group_size == 1:
                            genre_file.write(values.format(tabLine[0], "'" + genre + "'"))
                        else:
                            genre_file.write(", " + values.format(tabLine[0], "'" + genre + "'"))
                        
                        #genreList.add(genre)
                
                # On insÃ¨re la ligne avec le genre en moins
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
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("ALTER TABLE work_basics ADD PRIMARY KEY (id_work);\n")
            output_file.write("CREATE INDEX IX_worktype ON work_basics (worktype);\n")
            output_file.write("CREATE INDEX IX_originalTitle ON work_basics (originalTitle(50));\n")
            output_file.write("CREATE INDEX IX_startYear ON work_basics (startYear);\n")
            output_file.write("CREATE INDEX IX_runtimeMinutes ON work_basics (runtimeMinutes);\n")
            print("Fichier work_basics.sql crÃ©Ã©")
            genre_file.write("CREATE INDEX IX_id_work ON work_genres (id_work);\n")
            genre_file.write("CREATE INDEX IX_genre ON work_genres (genre);\n")
            print("Fichier work_genres.sql crÃ©Ã©")
            #print(cat)
            #print(genreList)




# title.principals.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# tconst (string) - alphanumeric unique identifier of the title
# ordering (integer) â€“ a number to uniquely identify rows for a given titleId
# nconst (string) - alphanumeric unique identifier of the name/person
# category (string) - the category of job that person was in
# job (string) - the specific job title if applicable, else '\N'
# characters (string) - the name of the character played if applicable, else '\N'
#
#
# Choix pour la base MySQLÂ :
#
# work_principals
# id_work : unsigned int
# ordering : unsigned tinyint (limitation Ã  10 par l'IMDB)
# id_person : unsigned int
# category : ENUM('archive_footage', 'editor', 'self', 'writer', 'production_designer', 'cinematographer', 'producer', 'casting_director', 'archive_sound', 'actor', 'director', 'actress', 'composer')
# job : varchar(500)
# characters : varchar(1400) [tableau des personnages : Ã  changer par la suite, mais c'est pas facileâ€¦]

def generateWorkPrincipals(group_size = 1000):
    print("CrÃ©ation de work_principals.sql")
    with open("title.principals.tsv", 'r', encoding="utf8") as file:
        with open('work_principals.sql', 'w', encoding="utf8") as output_file:
            
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_principals`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE IF NOT EXISTS `work_principals` (`id_work` INT UNSIGNED, `ordering` TINYINT UNSIGNED, `id_person` INT UNSIGNED, `category` ENUM('archive_footage', 'editor', 'self', 'writer', 'production_designer', 'cinematographer', 'producer', 'casting_director', 'archive_sound', 'actor', 'director', 'actress', 'composer'), `job` VARCHAR(500), `characters` VARCHAR(1400));\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            #cat = set()
            #max_size = 0
            nb = 0
            debut = time.perf_counter()
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `work_principals` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # Nettoyage des champs
                for i in range(3,len(tabLine)):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                    else: # On ajoute et on Ã©chappe les quotes (et les antislash)
                        tabLine[i] = "'"+ tabLine[i].replace("'", "''").replace("\\", "\\\\") + "'"
                #cat.add(tabLine[3])
                #if len(tabLine[5]) > max_size:
                #   max_size = len(tabLine[5])
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[2] = tabLine[2][2:].lstrip("0")

                
                # On insÃ¨re la ligne
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
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("CREATE UNIQUE INDEX UX_id_work_ordering ON work_principals (id_work, ordering);\n")
            output_file.write("CREATE INDEX IX_id_person ON work_principals (id_person);\n")
            
            print("Fichier work_principals.sql crÃ©Ã©")
            #print(cat)
            #print(max_size)



            
# title.akas.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# titleId (string) - a tconst, an alphanumeric unique identifier of the title
# ordering (integer) â€“ a number to uniquely identify rows for a given titleId
# title (string) â€“ the localized title
# region (string) - the region for this version of the title
# language (string) - the language of the title
# types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
# attributes (array) - Additional terms to describe this alternative title, not enumerated
# isOriginalTitle (boolean) â€“ 0: not original title; 1: original title
#
#
# Choix pour la base MySQLÂ :
#
# work_akas :
# id_work : unsigned int
# ordering : unsigned smallint
# title : varchar(1000)
# region : varchar(4)
# language : varchar(3)
# attributes : varchar(200)
# isOriginalTitle : tinyint
#
# work_types :
# id_work : unsigned int
# ordering : unsigned smallint
# type : ENUM('alternative', 'dvd', 'festival', 'tv', 'video', 'working', 'original', 'imdbDisplay')


def generateWorkAkas(group_size = 1000):
    print("CrÃ©ation de work_akas.sql et work_types.sql")
    with open("title.akas.tsv", 'r', encoding="utf8") as file:
        with open('work_akas.sql', 'w', encoding="utf8") as output_file, open('work_types.sql', 'w', encoding="utf8") as types_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_akas`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_akas` (id_work INT UNSIGNED, ordering SMALLINT UNSIGNED, title VARCHAR(1000), region VARCHAR(4), language VARCHAR(3), attributes VARCHAR(200), isOriginalTitle TINYINT);\n")
            
            # Suppression de la table
            types_file.write("DROP TABLE IF EXISTS `work_types`;\n")
            # CrÃ©ation de la table
            types_file.write("CREATE TABLE `work_types` (id_work INT UNSIGNED, ordering SMALLINT UNSIGNED, type ENUM('alternative', 'dvd', 'festival', 'tv', 'video', 'working', 'original', 'imdbDisplay'));\n")
            
            
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            nb_typ = 0
            #cat = set()
            debut = time.perf_counter()
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `work_akas` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (2, 3, 4, 5, 6):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                    else: # On ajoute et on Ã©chappe les quotes (et les antislash)
                        tabLine[i] = "'"+ tabLine[i].replace("'", "''").replace("\\", "\\\\") + "'"
                for i in (1, 7):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                # On enlÃ¨ve le sÃ©parateur bizarre de l'imdb et on le remplace par une virgule
                tabLine[5] = tabLine[5].replace("\x02",",")              
                #cat.add(tabLine[5])
                
                
                # On s'occupe des types
                if tabLine[5] != "NULL":
                    types = tabLine[5][1:-1].split(",")
                    for typ in types:
                        nb_typ += 1
                        if nb_typ % group_size == 1:
                            types_file.write("INSERT INTO `work_types` VALUES ")
                        values = "({}, {}, {})"
                        if nb_typ % group_size == 0:
                            types_file.write(", " + values.format(tabLine[0], tabLine[1], "'" + typ + "'")+";\n")
                        elif nb_typ % group_size == 1:
                            types_file.write(values.format(tabLine[0], tabLine[1], "'" + typ + "'"))
                        else:
                            types_file.write(", " + values.format(tabLine[0], tabLine[1], "'" + typ + "'"))
                        
                        
                # On insÃ¨re la ligne sans le type
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
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("CREATE UNIQUE INDEX UX_id_work_ordering ON work_akas (id_work, ordering);\n")
            print("Fichier work_akas.sql crÃ©Ã©")
            types_file.write("CREATE INDEX IX_id_work_ordering ON work_types (id_work, ordering);\n")
            print("Fichier work_types.sql crÃ©Ã©")
            #print(cat)


# title.ratings.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# tconst (string) - alphanumeric unique identifier of the title
# averageRating â€“ weighted average of all the individual user ratings
# numVotes - number of votes the title has received
#
#
# Choix pour la base MySQLÂ :
#
# work_ratings :
# id_work : unsigned int
# averageRating : decimal(3,1)
# numVotes : unsigned int
def generateWorkRatings(group_size = 1000):
    print("CrÃ©ation de work_ratings.sql")
    with open("title.ratings.tsv", 'r', encoding="utf8") as file:
        with open('work_ratings.sql', 'w', encoding="utf8") as output_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_ratings`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_ratings` (id_work INT UNSIGNED, averageRating DECIMAL(3,1), numVotes INT UNSIGNED);\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            debut = time.perf_counter()
            values = "({}, {}, {})"
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `work_ratings` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs
                for i in (1, 2):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                    #else: # On ajoute et on Ã©chappe les quotes
                        #tabLine[i] = "'"+ tabLine[i].replace("'", "''") + "'"
                
                # On insÃ¨re la ligne
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe        
            if nb % group_size != 0:
                output_file.write(";\n")
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("ALTER TABLE work_ratings ADD PRIMARY KEY (id_work);\n")
            print("Fichier work_ratings.sql crÃ©Ã©")


# title.episode.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# tconst (string) - alphanumeric identifier of episode
# parentTconst (string) - alphanumeric identifier of the parent TV Series
# seasonNumber (integer) â€“ season number the episode belongs to
# episodeNumber (integer) â€“ episode number of the tconst in the TV series
#
#
# Choix pour la base MySQLÂ :
#
# work_episode :
# id_work : unsigned int
# id_work_parent : unsigned int
# seasonNumber : unsigned smallint
# episodeNumber : unsigned mediumint
def generateWorkEpisode(group_size = 1000):
    print("CrÃ©ation de work_episode.sql")
    with open("title.episode.tsv", 'r', encoding="utf8") as file:
        with open('work_episode.sql', 'w', encoding="utf8") as output_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_episode`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_episode` (id_work INT UNSIGNED, id_work_parent INT UNSIGNED, seasonNumber SMALLINT UNSIGNED, episodeNumber MEDIUMINT UNSIGNED);\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            debut = time.perf_counter()
            #maxi = 0
            # Une accolade par champ
            values = "({}, {}, {}, {})"
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `work_episode` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                tabLine[1] = tabLine[1][2:].lstrip("0")
                # Nettoyage des champs (en Ã©vitant ceux qui sont des id si on peut)
                for i in range(2,len(tabLine)):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                    #else: # On ajoute et on Ã©chappe les quotes
                        #tabLine[i] = "'"+ tabLine[i].replace("'", "''") + "'"
                
                #if tabLine[i] != "NULL" and int(tabLine[3]) > maxi:
                #    maxi = int(tabLine[3])
                # On insÃ¨re la ligne
                if nb % group_size == 0:
                    output_file.write(", " + values.format(*tabLine)+";\n")
                elif nb % group_size == 1:
                    output_file.write(values.format(*tabLine))
                else:
                    output_file.write(", " + values.format(*tabLine))
            # Si nous n'avons pas fini un groupe        
            if nb % group_size != 0:
                output_file.write(";\n")
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("ALTER TABLE work_episode ADD PRIMARY KEY (id_work);\n")
            output_file.write("CREATE INDEX IX_id_work_parent ON work_episode (id_work_parent);\n")
            print("Fichier work_episode.sql crÃ©Ã©")
            #print(maxi)



# name.basics.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# nconst (string) - alphanumeric unique identifier of the name/person
# primaryName (string)â€“ name by which the person is most often credited
# birthYear â€“ in YYYY format
# deathYear â€“ in YYYY format if applicable, else '\N'
# primaryProfession (array of strings) â€“ the top-3 professions of the person
# knownForTitles (array of tconsts) â€“ titles the person is known for
#
#
# Choix pour la base MySQLÂ :
#
# name_basicsÂ :
# id_person : unsigned int primary key
# name : varchar(200)
# birthYear : smallint
# deathYear : smallint
#
# name_professionsÂ :
# id_person : unsigned int
# professionÂ : ENUM('music_department', 'podcaster', 'publicist', 'soundtrack', 'make_up_department', 'archive_footage', 'cinematographer', 'casting_director', 'production_manager', 'art_director', 'animation_department', 'actress', 'script_department', 'choreographer', 'editorial_department', 'accountant', 'talent_agent', 'executive', 'sound_department', 'set_decorator', 'producer', 'transportation_department', 'camera_department', 'location_management', 'director', 'composer', 'visual_effects', 'special_effects', 'legal', 'stunts', 'archive_sound', 'art_department', 'costume_designer', 'music_artist', 'production_designer', 'costume_department', 'actor', 'miscellaneous', 'casting_department', 'manager', 'assistant', 'electrical_department', 'assistant_director', 'production_department', 'writer', 'editor')
#
# name_knownForTitlesÂ :
# id_person : unsigned int
# id_workÂ : unsigned int

def generateNameBasics(group_size = 1000):
    print("CrÃ©ation de name_basics.sql, name_professions.sql et name_knownForTitles.sql")
    with open("name.basics.tsv", 'r', encoding="utf8") as file:
        with open('name_basics.sql', 'w', encoding="utf8") as output_file, open('name_professions.sql', 'w', encoding="utf8") as profession_file, open('name_knownForTitles.sql', 'w', encoding="utf8") as known_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `name_basics`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `name_basics` (id_person INT UNSIGNED, name VARCHAR(200), birthYear SMALLINT, deathYear SMALLINT);\n")
            
            # Professions
            # Suppression de la table
            profession_file.write("DROP TABLE IF EXISTS `name_professions`;\n")
            # CrÃ©ation de la table
            profession_file.write("CREATE TABLE `name_professions` (id_person INT UNSIGNED, profession ENUM('music_department', 'podcaster', 'publicist', 'soundtrack', 'make_up_department', 'archive_footage', 'cinematographer', 'casting_director', 'production_manager', 'art_director', 'animation_department', 'actress', 'script_department', 'choreographer', 'editorial_department', 'accountant', 'talent_agent', 'executive', 'sound_department', 'set_decorator', 'producer', 'transportation_department', 'camera_department', 'location_management', 'director', 'composer', 'visual_effects', 'special_effects', 'legal', 'stunts', 'archive_sound', 'art_department', 'costume_designer', 'music_artist', 'production_designer', 'costume_department', 'actor', 'miscellaneous', 'casting_department', 'manager', 'assistant', 'electrical_department', 'assistant_director', 'production_department', 'writer', 'editor'));\n")
            
            # knownForTitles
            # Suppression de la table
            known_file.write("DROP TABLE IF EXISTS `name_knownForTitles`;\n")
            # CrÃ©ation de la table
            known_file.write("CREATE TABLE `name_knownForTitles` (id_person INT UNSIGNED, id_work INT UNSIGNED);\n")
            
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            nb_prof = 0
            nb_known = 0
            debut = time.perf_counter()
            #maxi = 0
            #profList = set()
            
            for line in file:
                #if nb == 300:
                #    break
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                if nb % group_size == 1:
                    output_file.write("INSERT INTO `name_basics` VALUES ")
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs (en Ã©vitant ceux qui sont des id si on peut simplement)
                for i in (1, 4, 5):
                    if tabLine[i] == "\\N" or tabLine[i] =='': # On ajoute NULL
                        tabLine[i] = "NULL"
                    else: # On ajoute et on Ã©chappe les quotes (et les antislash)
                        tabLine[i] = "'"+ tabLine[i].replace("'", "''").replace("\\", "\\\\") + "'"
                for i in (2, 3):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                #if len(tabLine[5]) > maxi:
                #    maxi = len(tabLine[5])
                
                # On extrait toutes les professions
                if tabLine[4] != "NULL":
                    profs = tabLine[4][1:-1].split(",")
                    for prof in profs:
                        nb_prof += 1
                        if nb_prof % group_size == 1:
                            profession_file.write("INSERT INTO `name_professions` VALUES ")
                        values = "({}, {})"
                        if nb_prof % group_size == 0:
                            profession_file.write(", " + values.format(tabLine[0], "'" + prof + "'")+";\n")
                        elif nb_prof % group_size == 1:
                            profession_file.write(values.format(tabLine[0], "'" + prof + "'"))
                        else:
                            profession_file.write(", " + values.format(tabLine[0], "'" + prof + "'"))
                        #profList.add(prof)
                
                
                # On extrait les knownForTitles
                if tabLine[5] != "NULL":
                    known_ids = tabLine[5][1:-1].split(",") # On rÃ©cupÃ¨re les ids avec tt et les 0
                    for known_id in known_ids:
                        nb_known += 1
                        # On extrait l'id
                        known_id = known_id[2:].lstrip("0")
                        if nb_known % group_size == 1:
                            known_file.write("INSERT INTO `name_knownForTitles` VALUES ")
                        values = "({}, {})"
                        if nb_known % group_size == 0:
                            known_file.write(", " + values.format(tabLine[0], known_id)+";\n")
                        elif nb_known % group_size == 1:
                            known_file.write(values.format(tabLine[0], known_id))
                        else:
                            known_file.write(", " + values.format(tabLine[0], known_id))
                        
                
                
                # On insÃ¨re la ligne sans professio et knownForTitles
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
                
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("ALTER TABLE name_basics ADD PRIMARY KEY (id_person);\n")
            output_file.write("CREATE INDEX IX_name ON name_basics (name);\n") # Pour les recherches sur les noms
            print("Fichier name_basics.sql crÃ©Ã©")
            profession_file.write("CREATE INDEX IX_id_person ON name_professions (id_person);\n")
            profession_file.write("CREATE INDEX IX_profession ON name_professions (profession);\n")
            print("Fichier name_professions.sql crÃ©Ã©")
            known_file.write("CREATE INDEX IX_id_person ON name_knownForTitles (id_person);\n")
            known_file.write("CREATE INDEX IX_id_work ON name_knownForTitles (id_work);\n")
            print("Fichier name_knownForTitles.sql crÃ©Ã©")
            
            #print(maxi)
            #print(profList)


# title.crew.tsv
# --------------------
#
#
# Info de l'imdbÂ :
#
# tconst (string) - alphanumeric unique identifier of the title
# directors (array of nconsts) - director(s) of the given title
# writers (array of nconsts) â€“ writer(s) of the given title
#
#
# Choix pour la base MySQLÂ :
# Deux bases de liensÂ :
#
# work_director :
# id_work : unsigned int
# id_person : unsigned int
#
# work_writer :
# id_work : unsigned int
# id_person : unsigned int
def generateTitleCrew(group_size = 1000):
    print("CrÃ©ation de work_director.sql et work_writer.sql")
    # On fait deux passages pour simplifier
    
    # Directors
    with open("title.crew.tsv", 'r', encoding="utf8") as file:
        with open('work_director.sql', 'w', encoding="utf8") as output_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_director`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_director` (id_work INT UNSIGNED, id_person INT UNSIGNED);\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            # Une accolade par champ
            values = "({}, {})"
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs (en Ã©vitant ceux qui sont des id si on peut simplement)
                for i in range(1,len(tabLine)):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                
                if tabLine[1] != "NULL":
                    directors = tabLine[1].split(",")
                    #print(directors)
                    for director in directors:
                        nb_insert = nb_insert + 1
                        if nb_insert % group_size == 1:
                            output_file.write("INSERT INTO `work_director` VALUES ")
                        # On insÃ¨re la ligne
                        if nb_insert % group_size == 0:
                            output_file.write(", " + values.format(tabLine[0], director[2:].lstrip("0"))+";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values.format(tabLine[0], director[2:].lstrip("0")))
                        else:
                            output_file.write(", " + values.format(tabLine[0], director[2:].lstrip("0")))
                
            # Si nous n'avons pas fini un groupe        
            if nb_insert % group_size != 0:
                output_file.write(";\n")    
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("CREATE INDEX IX_id_work ON work_director (id_work);\n")
            output_file.write("CREATE INDEX IX_id_person ON work_director (id_person);\n")
            print("Fichier work_director.sql crÃ©Ã©")
            
    # Writers
    with open("title.crew.tsv", 'r', encoding="utf8") as file:
        with open('work_writer.sql', 'w', encoding="utf8") as output_file:
            # Suppression de la table
            output_file.write("DROP TABLE IF EXISTS `work_writer`;\n")
            # CrÃ©ation de la table
            output_file.write("CREATE TABLE `work_writer` (id_work INT UNSIGNED, id_person INT UNSIGNED);\n")
            
            # On Ã©vacue la premiÃ¨re ligne avec le nom des champs
            file.readline()
            
            # On parcourt toutes les lignes
            nb = 0
            nb_insert = 0
            debut = time.perf_counter()
            # Une accolade par champ
            values = "({}, {})"
            for line in file:
                nb += 1
                if nb % 100000 == 0:
                    fin = time.perf_counter()
                    temps = round(fin - debut)
                    print(nb, "lignes traitÃ©es en", temps, "secondes")
                    
                # On enlÃ¨ve le retour chariot
                cleanLine = line[:-1]
                #print(line)
                
                tabLine = cleanLine.split("\t")
                # On enlÃ¨ve les deux lettres au dÃ©but des identifiants
                tabLine[0] = tabLine[0][2:].lstrip("0")
                # Nettoyage des champs (en Ã©vitant ceux qui sont des id si on peut simplement)
                for i in range(1,len(tabLine)):
                    if tabLine[i] == "\\N": # On ajoute NULL
                        tabLine[i] = "NULL"
                
                if tabLine[2] != "NULL":
                    writers = tabLine[2].split(",")
                    #print(directors)
                    for writer in writers:
                        nb_insert = nb_insert + 1
                        if nb_insert % group_size == 1:
                            output_file.write("INSERT INTO `work_writer` VALUES ")
                        # On insÃ¨re la ligne
                        if nb_insert % group_size == 0:
                            output_file.write(", " + values.format(tabLine[0], writer[2:].lstrip("0"))+";\n")
                        elif nb_insert % group_size == 1:
                            output_file.write(values.format(tabLine[0], writer[2:].lstrip("0")))
                        else:
                            output_file.write(", " + values.format(tabLine[0], writer[2:].lstrip("0")))
                
            # Si nous n'avons pas fini un groupe        
            if nb_insert % group_size != 0:
                output_file.write(";\n")    
            # CrÃ©ation des index pour avoir des requÃªtes plus performantes
            output_file.write("CREATE INDEX IX_id_work ON work_writer (id_work);\n")
            output_file.write("CREATE INDEX IX_id_person ON work_writer (id_person);\n")
            print("Fichier work_writer.sql crÃ©Ã©")




# Lignes Ã  commenter pour ne pas faire tous les fichiers d'un coup

generateWorkBasics()
generateWorkPrincipals()
generateWorkAkas()
generateWorkRatings()
generateWorkEpisode()
generateNameBasics()
generateTitleCrew()

