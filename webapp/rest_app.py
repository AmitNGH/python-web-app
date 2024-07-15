from flask import Flask, jsonify, request
from datetime import datetime
from db_handler import db_connection

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    response = {}

    with db_connection().cursor() as cursor:
        cursor.execute(f"SELECT user_name "
                       f"FROM `users` "
                       f"WHERE `user_id`={user_id}")
        if cursor.rowcount == 0:
            response["status"] = "error"
            response["reason"] = "no such id"
            return_code = 500
        else:
            response["status"] = "ok"
            response["user_name"] = cursor.fetchone()
            return_code = 200

    return jsonify(response), return_code


@app.route(backend_route, methods=['POST'])
def create_user(user_id):
    request_payload = request.json()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = request_payload['user_name']

    # TODO: check if user with same id exists, Error handling

    with db_connection().cursor() as cursor:
        cursor.execute(f"INSERT INTO users (user_id, user_name, creation_date) "
                       f"VALUES ({user_id}, {user_name}, {now}")


@app.route(backend_route, methods=['PUT'])
def update_user(user_id):
    request_payload = request.json()
    user_name = request_payload['user_name']

    # TODO: Check if user exists before updating, Error handling

    with db_connection().cursor() as cursor:
        cursor.execute(f"UPDATE users "
                       f"SET user_name = {user_name} "
                       f"WHERE user_id = {user_id}")


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
