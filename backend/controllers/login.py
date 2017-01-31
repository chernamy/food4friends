from flask import *
import extensions
import messages

login = Blueprint('api/v1/login', __name__)
logout = Blueprint('api/v1/logout', __name__)

@login.route("/api/v1/login/", methods=["POST"])
def api_login():
    if "userid" not in request.json:
        return messages.BuildErrorMessage("Missing userid"), 422
    if "password" not in request.json:
        return messages.BuildErrorMessage("Missing password"), 422

    userid = request.json.get("userid")
    password = request.json.get("password")
    user_data = extensions.QueryUsers([("userid", userid),
                                        ("password", password)])
    if not user_data:
        return messages.BuildErrorMessage("Invalid login credentials"), 422

    session["userid"] = userid
    return messages.SUCCESS

@logout.route("/api/v1/logout/", methods=["POST"])
def api_logout():
    session.clear()
    return messages.SUCCESS
