from flask import Flask, jsonify, request

from db_connector import (get_existing_user_data,
                          create_new_user)

from Utils import (extract_json_from_request,
                   ok_response_template,
                   unprocessable_entity_response_template,
                   unsupported_media_type_response_template,
                   internal_server_error_response_template)
from webapp.Entity.User import User

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


# Returns username stored in the DB for a given id
@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    # Executes query to get the requested user from the database
    user = get_existing_user_data(user_id)

    # Checks if the user exists, building the response object accordingly
    if user:
        response, return_code = ok_response_template()
        response["user_name"] = user.user_name

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

    if create_new_user(User(user_id, user_name)):

        response, return_code = ok_response_template()
        response["user_added"] = user_name

    else:
        response, return_code = internal_server_error_response_template()
        response["reason"] = "id already exists"

    return jsonify(response), return_code


#
# @app.route(backend_route, methods=['PUT'])
# def update_user(user_id):
#     is_right_format, request_payload = extract_json_from_request(request)
#
#     if not is_right_format:
#         response, return_code = payload_not_type_json_response()
#
#         return jsonify(response), return_code
#
#     # Returns error is user_name key does not exist
#     user_name = request_payload.get("user_name")
#
#     if not user_name:
#         response, return_code = no_user_name_in_json_response()
#
#         return jsonify(response), return_code
#
#     with db_connection().cursor() as cursor:
#         user_exists = check_user_exists_by_id(user_id, cursor)
#
#         if user_exists:
#             cursor.execute(f"UPDATE users "
#                            f"SET user_name = '{user_name}' "
#                            f"WHERE user_id = {user_id}")
#             db_connection().commit()
#
#             response, return_code = ok_response_template()
#             response["user_updated"] = user_name
#
#         # In case the user does not exist
#         else:
#             response, return_code = no_such_id_response()
#
#     return jsonify(response), return_code
#
#
# @app.route(backend_route, methods=['DELETE'])
# def remove_user(user_id):
#     with db_connection().cursor() as cursor:
#         user_exists = check_user_exists_by_id(user_id, cursor)
#
#         if user_exists:
#             cursor.execute(f"DELETE FROM users "
#                            f"WHERE user_id = {user_id}")
#             db_connection().commit()
#
#             response, return_code = ok_response_template()
#             response["user_deleted"] = user_id
#         else:
#             response, return_code = no_such_id_response()
#
#     return jsonify(response), return_code
#

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


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
