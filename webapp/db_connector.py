from configparser import ConfigParser
from webapp.Entity.User import User
from Utils import (USER_ID_INDEX_IN_DB,
                   USER_NAME_INDEX_IN_DB,
                   CREATION_DATE_INDEX_IN_DB)

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


# Gets user_id and returns the user object if the user exists, False if the user does not exist
def get_existing_user_data(user_id) -> bool | type(User):
    with (connection.cursor() as cursor):
        user_exists, user_tuple = check_user_exists_by_id(user_id, cursor, True)
        if user_exists:
            return User(user_tuple[USER_ID_INDEX_IN_DB - 1],
                        user_tuple[USER_NAME_INDEX_IN_DB - 1],
                        user_tuple[CREATION_DATE_INDEX_IN_DB - 1])

        return False


def create_new_user(user):
    # Check id does not exist and execute insert to db
    with connection.cursor() as cursor:
        user_exists = check_user_exists_by_id(user.user_id, cursor)

        if not user_exists:
            cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                           f"VALUES ({user.user_id}, '{user.user_name}', '{user.creation_date}')")
            connection.commit()

            return True

        return False


# Runs a SELECT query on DB to check if the user_id exists
# Returns tuple containing if the user_id exists and the user dict in-case requested
def check_user_exists_by_id(user_id, cursor, return_user_object=False) -> bool | tuple[bool, dict]:
    connection.commit()
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


# # Returns the db connection instance
# def db_connection():
#     return connection
