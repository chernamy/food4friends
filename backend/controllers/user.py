from flask import *
import extensions
import messages

user = Blueprint("/api/v1/user", __name__)

@user.route("/api/v1/user", methods=["GET"])
@user.route("/api/v1/user/", methods=["GET"])
def GetUserData():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.args is None:
        return messages.NO_URL_PARAMETERS, 400

    if "userid" not in request.args:
        return messages.NO_URL_PARAMETERS, 400

    userid = request.args.get("userid")
    user_data = extensions.Query(extensions.UserData, [("userid", userid)])
    if not user_data:
        return messages.NONEXISTENT_USER, 400

    return messages.BuildUserInfoMessage(user_data[0]), 200
