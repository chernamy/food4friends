from flask import *

login = Blueprint('api/v1/login', __name__)

@login.route("/api/v1/login", methods=["POST"])
def api_login():
    return "You reached the test login route."
