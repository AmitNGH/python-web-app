from flask import Flask, jsonify, request
from datetime import datetime

from db_handler import db_connection
from Utils import (extract_json_from_request,
                   ok_response_template,
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
        user_exists, user_object = check_user_exists_by_id(user_id, cursor, True)

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

    # TODO: Extract duplicate code to method, use in POST, PUT
    is_right_format, request_payload = extract_json_from_request(request)

    # Returns error in-case request is not in json format
    if not is_right_format:
        response, return_code = unsupported_media_type_response_template()
        response["reason"] = "payload should be json"

        return jsonify(response), return_code

    # TODO: Extract duplicate code to method, use in POST, PUT
    # Returns error is user_name key does not exist
    user_name = request_payload.get("user_name")

    if not user_name:
        response, return_code = unprocessable_entity_response_template()
        response["reason"] = "json does not contain user_name"

        return jsonify(response), return_code

    # Check id does not exist and execute insert to db
    with db_connection().cursor() as cursor:
        user_exists = check_user_exists_by_id(user_id, cursor)

        if not user_exists:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                           f"VALUES ({user_id}, '{user_name}', '{now}')")

            db_connection().commit()

    if user_exists:
        response, return_code = internal_server_error_response_template()
        response["reason"] = "id already exists"
    else:
        response, return_code = ok_response_template()
        response["user_added"] = user_name

    return jsonify(response), return_code


@app.route(backend_route, methods=['PUT'])
def update_user(user_id):

    # TODO: Extract duplicate code to method, use in POST, PUT
    is_right_format, request_payload = extract_json_from_request(request)

    if not is_right_format:
        response, return_code = unsupported_media_type_response_template()
        response["reason"] = "payload should be json"

        return jsonify(response), return_code

    # TODO: Extract duplicate code to method, use in POST, PUT
    # Returns error is user_name key does not exist
    user_name = request_payload.get("user_name")

    if not user_name:
        response, return_code = unprocessable_entity_response_template()
        response["reason"] = "json does not contain user_name"

        return jsonify(response), return_code

    with db_connection().cursor() as cursor:
        user_exists = check_user_exists_by_id(user_id, cursor)

        if user_exists:
            cursor.execute(f"UPDATE users "
                           f"SET user_name = '{user_name}' "
                           f"WHERE user_id = {user_id}")
            db_connection().commit()

        # In case the user does not exist
        if user_exists:
            response, return_code = ok_response_template()
            response["user_updated"] = user_name
        else:
            response, return_code = internal_server_error_response_template()
            response["reason"] = "no such id"

    return jsonify(response), return_code


@app.route(backend_route, methods=['DELETE'])
def remove_user(user_id):
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users"
                       f"WHERE user_id = {user_id}")

        # TODO: Check if user exists before deleting, Error handling


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

    return False


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
