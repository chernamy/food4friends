from flask import *
import extensions
import messages

user = Blueprint("/api/v1/user", __name__)

@user.route("/api/v1/user", methods=["GET"])
@user.route("/api/v1/user/", methods=["GET"])
def GetUserData():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "userid" not in request.json:
        return messages.MISSING_USERID, 400

    userid = request.json.get("userid")
    user_data = extensions.QueryUsers([("userid", userid)])
    if not user_data:
        return messages.NONEXISTENT_USER, 400

    return messages.BuildUserInfoMessage(user_data[0]), 200
