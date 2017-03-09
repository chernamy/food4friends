from flask import *
import extensions
import messages

community = Blueprint("/api/v1/community/", __name__)
communities = Blueprint("/api/v1/communities/", __name__)

@communities.route("/api/v1/communities/", methods=["GET"])
def ViewCommunities():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    community_data = extensions.QueryCommunities()
    return messages.BuildCommunityListMessage(community_data), 200

@communities.route("/api/v1/communities/", methods=["POST"])
def CreateCommunity():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "communityname" not in request.json:
        return messages.MISSING_COMMUNITYNAME

    communityname = request.json.get("communityname")
    new_community = extensions.CommunityData(0, communityname)
    extensions.AddCommunity(new_community)

    # TODO (mjchao): Add user to the community just created.
    return messages.SUCCESS, 200

@communities.route("/api/v1/community", methods=["GET"])
def GetUsersInCommunity():
    pass

def AddUserToCommunity(userid, communityid):
    pass
    
@communities.route("/api/v1/community/", methods=["POST"])
def ProcessAddUserToCommunityRequest():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "userid" not in request.json:
        return messages.MISSING_ADD_USERID, 400

    if "communityname" not in request.json:
        return messages.MISSING_COMMUNITYNAME, 400
