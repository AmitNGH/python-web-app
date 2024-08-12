from signal import CTRL_C_EVENT
from os import kill, getpid
from flask import Flask
from webapp.Utils import (SignedIntConverter,
                          USER_NAME_INDEX_IN_DB)
from webapp.db_handler import (db_connection,
                               check_user_exists_by_id)

app = Flask(__name__)
app.url_map.converters['sint'] = SignedIntConverter


# Gets user data by given id as HTML format
@app.route("/users/get_user_data/<sint:user_id>")
def get_user_name(user_id):
    with db_connection().cursor() as cursor:
        user_exists, user_object = check_user_exists_by_id(user_id, cursor, return_user_object=True)

    if user_exists:
        return f"<H1 id='user'> {user_object[USER_NAME_INDEX_IN_DB - 1]} </H1>"
    else:
        return f"<H1 id='error'>no such user with id: {user_id}</H1>"


# Sends Ctrl C event to shutdown server
@app.route('/stop_server')
def stop_server():
    kill(getpid(), CTRL_C_EVENT)
    return 'Server stopped'


def run_web_app(debug_mode=False):
    app.run(host="0.0.0.0", port=5001, debug=debug_mode)


if __name__ == "__main__":
    run_web_app(True)
