from configparser import ConfigParser
import pymysql.cursors

config = ConfigParser()
config.read('config.ini')

connection = pymysql.connect(host=config['DB']['host'],
                             port=int(config['DB']['port']),
                             database=config['DB']['database'],
                             user=config['DB']['user'],
                             password=config['DB']['password'])


def db_connection():
    return connection
