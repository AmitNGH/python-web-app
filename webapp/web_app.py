from flask import Flask

app = Flask(__name__)


@app.route(endpoint="/users/get_user_data/<user_id>")
def get_user(user_id):
    print("Hello World")


def run_web_app():
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    run_web_app()
