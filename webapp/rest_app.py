from flask import Flask
from db_handler import db_connection

app = Flask(__name__)

backend_route = '/users/<user_id>'


@app.route(endpoint=backend_route, methods=['GET'])
def get_user(user_id):
    with db_connection().cursor() as cursor:
        cursor.execute(f"SELECT user_name FROM `users` WHERE `id`={user_id}")


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
