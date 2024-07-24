from flask import Flask, jsonify, request
from datetime import datetime

from werkzeug.exceptions import UnsupportedMediaType

from db_handler import db_connection
from Utils import (ok_response_template,
                   unprocessable_entity_response_template,
                   unsupported_media_type_response_template,
                   internal_server_error_response_template,
                   USER_NAME_INDEX_IN_DB)

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


# Returns username stored in the DB for a given id
@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    # Executes query to get the requested user from the database
    with db_connection().cursor() as cursor:
        user_exists, user_object = check_user_exists_by_id(user_id, cursor)

    # Checks if the user exists, building the response object accordingly
    if user_exists:
        response, return_code = ok_response_template()
        response["user_name"] = user_object[USER_NAME_INDEX_IN_DB - 1]

    else:
        response, return_code = internal_server_error_response_template()
        response["reason"] = "no such id"

    return jsonify(response), return_code


# Saves new user to DB for a given id and json payload containing key user_name
@app.route(backend_route, methods=['POST'])
def create_user(user_id):

    is_right_format, request_payload = extract_json_from_request(request)

    # Returns error in-case request is not in json format
    if not is_right_format:
        response, return_code = unsupported_media_type_response_template()
        response["reason"] = "payload should be json"

        return jsonify(response), return_code

    # Returns error is user_name key does not exist
    user_name = request_payload.get("user_name")

    if not user_name:
        response, return_code = unprocessable_entity_response_template()
        response["reason"] = "json does not contain user_name"

        return jsonify(response), return_code

    # Check id does not exist and execute insert to db
    with db_connection().cursor() as cursor:
        id_exists, user_data = check_user_exists_by_id(user_id, cursor)

        if not id_exists:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                           f"VALUES ({user_id}, '{user_name}', '{now}')")

            db_connection().commit()

    if id_exists:
        response, return_code = internal_server_error_response_template()
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


#
def check_user_exists_by_id(user_id, cursor) -> tuple[bool, dict]:
    cursor.execute(f"SELECT user_id, user_name, creation_date "
                   f"FROM users "
                   f"WHERE user_id={user_id}")

    if cursor.rowcount:
        return True, cursor.fetchone()

    return False, {}


# Attempts to extract json object from given request -
# Returns tuple containing if the operation was successful and the extracted json object
def extract_json_from_request(json_request) -> tuple[bool, dict]:
    try:
        request_json = json_request.get_json()
    except UnsupportedMediaType:
        return False, {}

    return True, request_json


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
