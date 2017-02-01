from flask import *
import extensions
import messages

login = Blueprint("api/v1/login/", __name__)
logout = Blueprint("api/v1/logout/", __name__)

@login.route("/api/v1/login/", methods=["POST"])
def Login():
    if "userid" not in request.json:
        return messages.MISSING_USERID, 400

    if "userid" in session:
        return messages.ALREADY_LOGGED_IN, 401
    
    userid = request.json.get("userid")
    user_data = extensions.QueryUsers([("userid", userid)])

    if not user_data:
        return messages.INVALID_CREDENTIALS, 422

    session["userid"] = userid
    return messages.SUCCESS, 200

@logout.route("/api/v1/logout/", methods=["POST"])
def Logout():
    if not "userid" in session:
        return messages.NOT_LOGGED_IN, 401

    session.clear()
    return messages.SUCCESS, 200
