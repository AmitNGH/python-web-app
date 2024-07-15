from flask import Flask, jsonify, request
from datetime import datetime
from pymysql import IntegrityError

from db_handler import db_connection
from Utils import PYMYSQL_DUPLICATE_ERROR

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    response = {}

    # Executes query to get the requested user from the database
    with db_connection().cursor() as cursor:
        cursor.execute(f"SELECT user_name "
                       f"FROM `users` "
                       f"WHERE `user_id`={user_id}")

        # In case the user does not exist
        if cursor.rowcount == 0:
            response["status"] = "error"
            response["reason"] = "no such id"
            return_code = 500
        else:
            response["status"] = "ok"
            response["user_name"] = cursor.fetchone()[0]
            return_code = 200

    return jsonify(response), return_code


@app.route(backend_route, methods=['POST'])
def create_user(user_id):
    # Get payload from request
    request_payload = request.get_json()

    # Prepare data for query
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = request_payload['user_name']

    response = {}
    id_exists = False

    with db_connection().cursor() as cursor:
        try:
            cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                           f"VALUES ({user_id}, '{user_name}', '{now}')")
        except IntegrityError as e:
            if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
                id_exists = True

    if id_exists:
        response["status"] = "error"
        response["reason"] = "id already exists"
        return_code = 500
    else:
        db_connection().commit()
        response["status"] = "ok"
        response["user_added"] = user_name
        return_code = 200

    return jsonify(response), return_code


@app.route(backend_route, methods=['PUT'])
def update_user(user_id):
    # Get payload from request
    request_payload = request.get_json()

    # Prepare data for query
    user_name = request_payload['user_name']

    response = {}

    with db_connection().cursor() as cursor:
        cursor.execute(f"UPDATE users "
                       f"SET user_name = '{user_name}' "
                       f"WHERE user_id = {user_id}")

        # TODO: Add id exists check, and add it to previous methods
        # In case the user does not exist
        if cursor.rowcount == 0:
            response["status"] = "error"
            response["reason"] = "no such id"
            return_code = 500
        else:
            db_connection().commit()
            response["status"] = "ok"
            response["user_updated"] = cursor.fetchone()[0]
            return_code = 200

    return jsonify(response), return_code


@app.route(backend_route, methods=['DELETE'])
def remove_user(user_id):
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users"
                       f"WHERE user_id = {user_id}")

        # TODO: Check if user exists before deleting, Error handling


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
