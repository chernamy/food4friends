from flask import *
import extensions
import messages

community = Blueprint("/api/v1/community/", __name__)
communities = Blueprint("/api/v1/communities/", __name__)

@communities.route("/api/v1/communities/", methods=["GET"])
def ViewCommunities():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    community_data = extensions.Query(extensions.CommunityData)
    return messages.BuildCommunityListMessage(community_data), 200

@communities.route("/api/v1/communities/", methods=["POST"])
def CreateCommunity():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "communityname" not in request.json:
        return messages.MISSING_COMMUNITYNAME

    communityname = request.json.get("communityname")
    new_community = extensions.CommunityData(0, communityname)
    extensions.Insert(new_community)

    # Add user to the community just created.
    # The new communityid is autoincremented, so its ID should 
    userid = session["userid"]
    new_community_id = extensions.GetLastAutoIncID()
    AddUserToCommunity(userid, new_community_id)
    return messages.SUCCESS, 200

@community.route("/api/v1/community/", methods=["GET"])
def GetUsersInCommunity():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "communityid" not in request.json:
        return messages.MISSING_COMMUNITYID, 400

    communityid = request.json.get("communityid")
    communities = extensions.Query(extensions.MembershipData,
                                    [("communityid", communityid)])
    return messages.BuildMembersListMessage(communities), 200
        

def AddUserToCommunity(userid, communityid):
    new_membership = extensions.MembershipData(userid, communityid)
    extensions.Insert(new_membership)
    
@community.route("/api/v1/community/", methods=["POST"])
def ProcessAddUserToCommunityRequest():
    # TODO (mjchao): Test this function
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "userid" not in request.json:
        return messages.MISSING_ADD_USERID, 400

    if "communityid" not in request.json:
        return messages.MISSING_COMMUNITYID, 400

    userid = request.json.get("userid")
    communityid = request.json.get("communityid")

    if extensions.Query(extensions.MEMBERSHIP_DATA,
                        [("userid", userid), ("communityid", communityid)]):
        return messages.DUPLICATE_MEMBERSHIP, 400

    AddUserToCommunity(userid, communityid)
