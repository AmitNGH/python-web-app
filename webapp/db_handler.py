from configparser import ConfigParser
import pymysql.cursors
import os

# This script reads connection details from config,
# establishes a connection with the db and returns the connection object
config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Connecting to DB
connection = pymysql.connect(host=config['DB']['host'],
                             port=int(config['DB']['port']),
                             database=config['DB']['database'],
                             user=config['DB']['user'],
                             password=config['DB']['password'])


# Runs a SELECT query on DB to check if the user_id exists
# Returns tuple containing if the user_id exists and the user object in-case requested
def check_user_exists_by_id(user_id, cursor, return_user_object=False) -> bool | tuple[bool, dict]:
    db_connection().commit()
    if return_user_object:
        cursor.execute(f"SELECT user_id, user_name, creation_date "
                       f"FROM users "
                       f"WHERE user_id={user_id}")
    else:
        cursor.execute(f"SELECT user_id "
                       f"FROM users "
                       f"WHERE user_id={user_id}")
    if cursor.rowcount:
        return True if not return_user_object else (True, cursor.fetchone())

    return False if not return_user_object else (False, {})


# Returns the db connection instance
def db_connection():
    return connection
