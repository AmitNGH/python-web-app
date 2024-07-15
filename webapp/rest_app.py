from flask import Flask, jsonify
from db_handler import db_connection

app = Flask(__name__)

backend_route = '/users/<int:user_id>'


@app.route(backend_route, methods=['GET'])
def get_user(user_id):
    response = {}

    with db_connection().cursor() as cursor:
        cursor.execute(f"SELECT user_name FROM `users` WHERE `user_id`={user_id}")
        if cursor.rowcount == 0:
            response["status"] = "error"
            response["reason"] = "no such id"
            return_code = 500
        else :
            response["status"] = "ok"
            response["user_name"] = cursor.fetchone()
            return_code = 200

    return jsonify(response), return_code


@app.route(backend_route, methods=['POST'])
def create_user(user_id):
    print("Hello World")


@app.route(backend_route, methods=['PUT'])
def update_user(user_id):
    print("Hello World")


@app.route(backend_route, methods=['DELETE'])
def remove_user(user_id):
    print("Hello World")


def run_rest_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_rest_app()
