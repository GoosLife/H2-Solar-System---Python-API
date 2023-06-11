import configparser
from  collections import namedtuple

config = configparser.ConfigParser()
config.read("config.ini")

DBConfig = namedtuple('DBConfig', ['DB_USER', 'DB_PASS', 'DB_SERV', 'DB_NAME']);

db_config = DBConfig(
    DB_USER=config['Database']['DB_USER'],
    DB_PASS=config['Database']['DB_PASS'],
    DB_SERV=config['Database']['DB_SERV'],
    DB_NAME=config['Database']['DB_NAME']
    )