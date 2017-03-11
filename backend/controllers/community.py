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

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "communityname" not in request.json:
        return messages.MISSING_COMMUNITYNAME, 400

    communityname = request.json.get("communityname")
    new_community = extensions.CommunityData(0, communityname)
    extensions.Insert(new_community)

    # Add user to the community just created.
    # The new communityid is autoincremented, so its ID should 
    userid = session["userid"]
    new_community_id = extensions.GetLastAutoIncID()
    AddUserToCommunity(userid, new_community_id, "joined")
    return messages.SUCCESS, 200


@communities.route("/api/v1/communities/joined/", methods=["GET"])
def GetJoinedCommunities():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    userid = session["userid"]
    joined_communities = extensions.Query(extensions.MembershipData,
                                [("userid", userid), ("status", "joined")])
    rtn_communities = []
    for community in joined_communities:
        rtn_communities.extend(extensions.Query(extensions.CommunityData,
                [("communityid", community.communityid)]))

    return messages.BuildCommunityListMessage(rtn_communities)
        

@communities.route("/api/v1/communities/invites/", methods=["GET"])
def GetInvitedCommunities():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    userid = session["userid"]
    invites = extensions.Query(extensions.MembershipData,
                                [("userid", userid), ("status", "pending")])
    communities = []
    for invite in invites:
        communities.extend(extensions.Query(extensions.CommunityData,
                            [("communityid", invite.communityid)]))

    return messages.BuildCommunityListMessage(communities)


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
        

def InSameCommunity(userid1, userid2):
    user1_community_ids = set([community.communityid for community in
                            extensions.Query(extensions.MembershipData,
                            [("userid", userid1), ("status", "joined")])])
    user2_communities = extensions.Query(extensions.MembershipData,
            [("userid", userid2), ("status", "joined")])

    for community in user2_communities:
        if community.communityid in user1_community_ids:
            return True

    return False

def AddUserToCommunity(userid, communityid, status):
    new_membership = extensions.MembershipData(userid, communityid, status)
    extensions.Insert(new_membership)
    

@community.route("/api/v1/community/add/", methods=["POST"])
def ProcessAddUserToCommunityRequest():
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

    if not extensions.Query(extensions.MembershipData,
                            [("userid", session["userid"]),
                            ("communityid", communityid),
                            ("status", "joined")]):
        return messages.NOT_IN_COMMUNITY, 403

    if extensions.Query(extensions.MembershipData,
                        [("userid", userid), ("communityid", communityid)]):
        return messages.DUPLICATE_MEMBERSHIP, 400

    AddUserToCommunity(userid, communityid, "pending")
    return messages.SUCCESS, 200


@community.route("/api/v1/community/join/", methods=["POST"])
def AcceptInvitationRequest():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400
    
    if "communityid" not in request.json:
        return messages.MISSING_COMMUNITYID, 400

    userid = session["userid"]
    communityid = request.json.get("communityid")

    invite = extensions.Query(extensions.MembershipData,
                            [("userid", userid), ("communityid", communityid),
                            ("status", "pending")])
    if not invite:
        return messages.NOT_INVITED

    extensions.Update(invite[0], "status='joined'")
    return messages.SUCCESS, 200
    
@community.route("/api/v1/community/leave/", methods=["DELETE"])
def LeaveCommunity():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "communityid" not in request.json:
        return messages.MISSING_COMMUNITYID, 400

    userid = session["userid"]
    communityid = request.json.get("communityid")

    membership = extensions.Query(extensions.MembershipData,
                                    [("userid", userid),
                                    ("communityid", communityid),
                                    ("status", "joined")])
    if not membership:
        return messages.NOT_IN_COMMUNITY

    extensions.Delete(membership[0])
    return messages.SUCCESS, 200
