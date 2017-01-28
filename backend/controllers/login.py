from flask import *
import extensions
import messages

login = Blueprint('api/v1/login', __name__)
logout = Blueprint('api/v1/logout', __name__)

@login.route("/api/v1/login", methods=["POST"])
def api_login():
    if "username" not in request.json:
        return messages.BuildErrorMessage("Missing username"), 422
    if "password" not in request.json:
        return messages.BuildErrorMessage("Missing password"), 422

    username = request.json.get("username")
    password = request.json.get("password")
    user_data = extensions.query_users([("username", username),
                                        ("password", password)])
    if not user_data:
        return messages.BuildErrorMessage("Invalid login credentials"), 422

    print "Returning"
    session["username"] = username
    return messages.BuildInfoMessage("Successfully logged in as %s" %(username))

@logout.route("/api/v1/logout", methods=["POST"])
def api_logout():
    session.clear()
    return messages.BuildInfoMessage("Successfully logged out")
