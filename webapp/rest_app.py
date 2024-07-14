from flask import Flask, jsonify
from db_handler import db_connection

app = Flask(__name__)

backend_route = '/users/<user_id>'


@app.route(endpoint=backend_route, methods=['GET'])
def get_user(user_id):
    try:
        user_id = int(user_id)

    except ValueError:
        # TODO: handle convert to int failed
        return_code = 500

    else:
        with db_connection().cursor() as cursor:
            cursor.execute(f"SELECT user_name FROM `users` WHERE `id`={user_id}")

        return_code = 200
        result = cursor.fetchone()

    return jsonify(result), return_code


@app.route(endpoint=backend_route, methods=['POST'])
def create_user(user_id):
    print("Hello World")


@app.route(endpoint=backend_route, methods=['PUT'])
def update_user(user_id):
    print("Hello World")


@app.route(endpoint=backend_route, methods=['DELETE'])
def remove_user(user_id):
    print("Hello World")


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
