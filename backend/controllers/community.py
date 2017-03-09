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
    return messages.SUCCESS, 200
    
