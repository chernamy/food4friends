from flask import *
import config
import extensions
import fb
import messages
import utils

login = Blueprint("api/v1/login/", __name__)
logout = Blueprint("api/v1/logout/", __name__)

@login.route("/api/v1/login/", methods=["POST"])
@utils.ssl_required
def Login():
    if request.json is None:
        return messages.NO_JSON_DATA

    if "userid" not in request.json:
        return messages.MISSING_USERID, 400

    if "token" not in request.json:
        return messages.MISSING_ACCESS_TOKEN, 400

    if "userid" in session:
        return messages.ALREADY_LOGGED_IN, 401
    
    userid = request.json.get("userid")
    access_token = request.json.get("token")

    if fb.VerifyAccessToken(userid, access_token):
        session["fb_access_token"] = access_token
        session["userid"] = userid

        user_data = extensions.Query(extensions.UserData, [("userid", userid)])

        # if user doesn't exist, create a new one and by default put in the
        # first community
        if not user_data:
            new_user_data = extensions.UserData(userid, "none", "-")
            extensions.Insert(new_user_data)
            default_community_membership = extensions.MembershipData(userid,
                    1, "joined")
            extensions.Insert(default_community_membership)

        return messages.SUCCESS, 200
    else:
        return messages.INVALID_CREDENTIALS, 422


@logout.route("/api/v1/logout/", methods=["POST"])
def Logout():
    if not "userid" in session:
        return messages.NOT_LOGGED_IN, 401

    session.clear()
    return messages.SUCCESS, 200
