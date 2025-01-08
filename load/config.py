import configparser
import os

###################################################################################


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)



###################################################################################

NEO4J_HOST = config["neo4j_database"]["host"]
NEO4J_AUTH = (
    config["neo4j_database"]["user"],
    config["neo4j_database"]["password"]
)

#########################################

PG_HOST = config["pg_database"]["host"]
PG_DB = config["pg_database"]["database"]
PG_USER = config["pg_database"]["user"]
PG_PASSWORD = config["pg_database"]["password"]
