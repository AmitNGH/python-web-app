from flask import Flask

webapp = Flask(__name__)


@webapp.route("/")
def hello_world():
    print("Hello World")
