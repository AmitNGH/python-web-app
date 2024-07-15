from configparser import ConfigParser
import pymysql.cursors

# This script reads connection details from config,
# establishes a connection with the db and returns the connection object
config = ConfigParser()
config.read('config.ini')

# Connecting to DB
connection = pymysql.connect(host=config['DB']['host'],
                             port=int(config['DB']['port']),
                             database=config['DB']['database'],
                             user=config['DB']['user'],
                             password=config['DB']['password'])

# Returns the db connection instance
def db_connection():
    return connection
