from signal import CTRL_C_EVENT
from os import kill, getpid
from flask import Flask, jsonify, request
from datetime import datetime

from db_handler import (db_connection,
                        check_user_exists_by_id)
from Utils import (SignedIntConverter,
                   extract_json_from_request,
                   ok_response_template,
                   unprocessable_entity_response_template,
                   unsupported_media_type_response_template,
                   internal_server_error_response_template,
                   USER_NAME_INDEX_IN_DB)

app = Flask(__name__)

app.url_map.converters['sint'] = SignedIntConverter
backend_route = '/users/<sint:user_id>'


# Returns username stored in the DB for a given id
@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    # Executes query to get the requested user from the database
    with db_connection().cursor() as cursor:
        (user_exists, user_object) = check_user_exists_by_id(user_id, cursor, True)

    # Checks if the user exists, building the response object accordingly
    if user_exists:
        response, return_code = ok_response_template()
        response["user_name"] = user_object[USER_NAME_INDEX_IN_DB - 1]

    else:
        response, return_code = no_such_id_response()

    return jsonify(response), return_code


# Saves new user to DB for a given id and json payload containing key user_name
@app.route(backend_route, methods=['POST'])
def create_user(user_id):
    is_right_format, request_payload = extract_json_from_request(request)

    # Returns error in-case request is not in json format
    if not is_right_format:
        response, return_code = payload_not_type_json_response()

        return jsonify(response), return_code

    # Returns error is user_name key does not exist
    user_name = request_payload.get("user_name")

    if not user_name:
        response, return_code = no_user_name_in_json_response()

        return jsonify(response), return_code

    # Check id does not exist and execute insert to db
    with db_connection().cursor() as cursor:
        user_exists = check_user_exists_by_id(user_id, cursor)
        user_db_id = user_id

        while user_exists:
            user_db_id += 1
            user_exists = check_user_exists_by_id(user_db_id, cursor)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, %s)", (user_db_id, user_name, now))
        db_connection().commit()

    response, return_code = ok_response_template()
    response["user_added"] = user_name
    response["user_id"] = user_db_id

    return jsonify(response), return_code


# Updates an existing user for a given id and json payload containing key user_name
@app.route(backend_route, methods=['PUT'])
def update_user(user_id):
    is_right_format, request_payload = extract_json_from_request(request)

    if not is_right_format:
        response, return_code = payload_not_type_json_response()

        return jsonify(response), return_code

    # Returns error is user_name key does not exist
    user_name = request_payload.get("user_name")

    if not user_name:
        response, return_code = no_user_name_in_json_response()

        return jsonify(response), return_code

    with db_connection().cursor() as cursor:
        user_exists = check_user_exists_by_id(user_id, cursor)

        if user_exists:
            cursor.execute("UPDATE users "
                           "SET user_name = %s "
                           "WHERE user_id = %s", (user_name, user_id))
            db_connection().commit()

            response, return_code = ok_response_template()
            response["user_updated"] = user_name

        # In case the user does not exist
        else:
            response, return_code = no_such_id_response()

    return jsonify(response), return_code


# Deletes existing user with the id provided
@app.route(backend_route, methods=['DELETE'])
def remove_user(user_id):
    with db_connection().cursor() as cursor:
        user_exists = check_user_exists_by_id(user_id, cursor)

        # if the user exists, deletes it from DB
        if user_exists:
            cursor.execute("DELETE FROM users "
                           "WHERE user_id = %s", user_id)
            db_connection().commit()

            response, return_code = ok_response_template()
            response["user_deleted"] = user_id
        else:
            response, return_code = no_such_id_response()

    return jsonify(response), return_code


def no_such_id_response():
    response, return_code = internal_server_error_response_template()
    response["reason"] = "no such id"

    return response, return_code


def no_user_name_in_json_response():
    response, return_code = unprocessable_entity_response_template()
    response["reason"] = "json does not contain user_name"

    return response, return_code


def payload_not_type_json_response():
    response, return_code = unsupported_media_type_response_template()
    response["reason"] = "payload should be json"

    return response, return_code


# Sends Ctrl C event to shutdown server
@app.route('/stop_server')
def stop_server():
    kill(getpid(), CTRL_C_EVENT)
    return 'Server stopped'


def run_rest_app(debug_mode=False):
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)


if __name__ == "__main__":
    run_rest_app(False)
