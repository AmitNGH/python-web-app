from flask import Flask, jsonify, request
from datetime import datetime

from db_handler import db_connection
from Utils import ERROR_RETURN_CODE, OK_RETURN_CODE

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    # Executes query to get the requested user from the database
    with db_connection().cursor() as cursor:
        user_exists, user_object = check_user_exists_by_id(user_id, cursor)

    # Checks if the user exists, building the response object accordingly
    if user_exists:
        response, return_code = ok_response_template()
        response["user_name"] = cursor.fetchone()[0]

    else:
        response, return_code = error_response_template()
        response["reason"] = "no such id"

    return jsonify(response), return_code


@app.route(backend_route, methods=['POST'])
def create_user(user_id):
    # Get payload from request
    request_payload = request.get_json()

    # Prepare data for query
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = request_payload['user_name']

    response = {}

    with db_connection().cursor() as cursor:
        id_exists, user_data = check_user_exists_by_id(user_id, cursor)

        if not id_exists:
            cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                           f"VALUES ({user_id}, '{user_name}', '{now}')")
            db_connection().commit()

    if id_exists:
        response, return_code = error_response_template()
        response["reason"] = "id already exists"
    else:
        response, return_code = ok_response_template()
        response["user_added"] = user_name

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


def check_user_exists_by_id(user_id, cursor) -> (bool, dict):
    cursor.execute(f"SELECT * "
                   f"FROM users "
                   f"WHERE user_id={user_id}")

    if cursor.rowcount:
        return True, cursor.fetchone()

    return False, {}


def error_response_template() -> (dict, int):
    return {'status': 'error'}, ERROR_RETURN_CODE


def ok_response_template() -> (dict, int):
    return {'status': 'ok'}, OK_RETURN_CODE


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
