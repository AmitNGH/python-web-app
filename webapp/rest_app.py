from flask import Flask

app = Flask(__name__)

users_by_id_route = '/users/<user_id>'


@app.route(endpoint=users_by_id_route, methods=['GET'])
def get_user(user_id):
    print("Hello World")


@app.route(endpoint=users_by_id_route, methods=['POST'])
def create_user(user_id):
    print("Hello World")


@app.route(endpoint=users_by_id_route, methods=['PUT'])
def update_user(user_id):
    print("Hello World")


@app.route(endpoint=users_by_id_route, methods=['DELETE'])
def remove_user(user_id):
    print("Hello World")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)