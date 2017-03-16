import extensions
import json

def BuildErrorMessage(error):
    msg = {
        "error": error
    }
    return json.dumps(msg)

def BuildInfoMessage(info):
    msg = {
        "info": info
    }
    return json.dumps(msg)

def BuildUserInfoMessage(user):
    msg = {
        "user": user.__dict__
    }
    return json.dumps(msg)

def UnwrapUserInfoMessage(msg):
    user_data = json.loads(msg)["user"]
    return extensions.UserData.FromDict(user_data)

def BuildItemListMessage(items):
    msg = {
        "items": [item.__dict__ for item in items]
    }
    return json.dumps(msg)

def UnwrapItemListMessage(msg):
    items = json.loads(msg)["items"]
    return [extensions.ItemData.FromDict(item_dict) for item_dict in items]

def BuildCommunityListMessage(communities):
    msg = {
        "communities": [community.__dict__ for community in communities]
    }
    return json.dumps(msg)

def UnwrapCommunityListMessage(msg):
    communities = json.loads(msg)["communities"]
    return [extensions.CommunityData.FromDict(community_dict) for
            community_dict in communities]

def BuildMembersListMessage(members):
    msg = {
        "members": [member.userid for member in members]
    }
    return json.dumps(msg)

def UnwrapMembersListMessage(msg):
    members = json.loads(msg)["members"]
    return [member_userid for member_userid in members]

def BuildRatingsListMessage(ratings):
    rating_sum = 0
    for rating in ratings:
        rating_sum += int(rating.rating)
    
    if len(ratings) == 0:
        average_rating = 0
    else:
        average_rating = float(rating_sum) / len(ratings)

    last_five_ratings = ratings[-5:]

    msg = {
        "average": average_rating,
        "ratings": [rating.__dict__ for rating in last_five_ratings]
    }
    return json.dumps(msg)

def UnwrapRatingListMessage(msg):
    msg_dict = json.loads(msg)
    return (msg_dict["average"],
            [extensions.RatingData.FromDict(rating_dict) for
            rating_dict in msg_dict(["ratings"])])


# ---- General Error Messages ---- #
SUCCESS = BuildInfoMessage("Success")
NOT_LOGGED_IN = BuildErrorMessage("You are not logged in.")
NO_JSON_DATA = BuildErrorMessage("Your request has no JSON data.")

# ---- Login Request Error Messages ---- #
MISSING_USERID = BuildErrorMessage("Missing userid")
MISSING_ACCESS_TOKEN = BuildErrorMessage("Missing access token")
INVALID_CREDENTIALS = BuildErrorMessage("Invalid credentials")
ALREADY_LOGGED_IN = BuildErrorMessage("You're already logged in. Logout first.")

# ---- User Request Error Messages ---- #
# Repeat: MISSING_USERID
NONEXISTENT_USER = BuildErrorMessage("User does not exist")

# ---- Buy Request Error Messages ---- #
# Repeat: NOT_LOGGED_IN
BUY_WRONG_USERID = BuildErrorMessage("You cannot buy on behalf of another user.")
MISSING_SELLERID = BuildErrorMessage("Missing sellerid field")
MISSING_BUYERID = BuildErrorMessage("Missing buyerid field")
MISSING_SERVINGS = BuildErrorMessage("Missing servings field")
INVALID_SERVINGS = BuildErrorMessage("Invalid servings field "\
                                        "(must be positive integer)")
NONEXISTENT_SELLER = BuildErrorMessage("No sell offer for given sellerid field")
TOO_MANY_SERVINGS = BuildErrorMessage("Servings field too large for sell offer")
OFFER_EXPIRED = BuildErrorMessage("Offer has already expired")
NOT_IN_SAME_COMMUNITY = BuildErrorMessage("You are not in the same community " \
                                            "as the seller.")
INVALID_USER_ROLE = BuildErrorMessage("You are already a buyer or seller. " \
                    "Finish that transaction before making a new sell offer.")

# ---- Sell Request Error Messages ---- #
# Repeat: MISSING_USERID
MISSING_PHOTO = BuildErrorMessage("Missing photo")
# Repeat: MISSING_SERVINGS
MISSING_DURATION = BuildErrorMessage("Missing duration")
MISSING_PRICE = BuildErrorMessage("Missing price")
MISSING_ADDRESS = BuildErrorMessage("Missing address")
MISSING_DESCRIPTION = BuildErrorMessage("Missing description")
# Repeat: INVALID_SERVINGS
INVALID_PHOTO_EXT = BuildErrorMessage("Invalid photo extension. Must be "\
                                        "png, jpg, jpeg, or gif.")
INVALID_DURATION = BuildErrorMessage("Invalid duration field " \
                                        "(must be positive integer)")
INVALID_PRICE = BuildErrorMessage("Invalid price (must be nonnegative decimal" \
                            " with at most two digits after the decimal place)")
# Repeat: INVALID_USER_ROLE


# ---- Complete Transaction Error Messages ---- #
# Repeat: MISSING_USERID
# Repeat: MISSING_BUYERID
NOT_SELLER = BuildErrorMessage("You must be a seller to perform this action.")
NONEXISTENT_BUYER = BuildErrorMessage("buyerid does not exist")
NOT_BUYER = BuildErrorMessage("The user with the given buyerid is not a buyer.")
NONEXISTENT_TRANSACTION = BuildErrorMessage("The specified transaction does " \
                                            "not exist.")

# ---- Edit Transaction Error Messages ---- #
# Repeat: NOT_LOGGED_IN
# Repeat: MISSING_USERID
# Repeat: NOT_SELLER
# Repeat: INVALID_PHOTO_EXT
INVALID_DELTA_SERVINGS = BuildErrorMessage("servings must be an integer.")
NEGATIVE_SERVINGS = BuildErrorMessage("Cannot reduce servings to a negative " \
                                        "amount.")
INVALID_DELTA_DURATION = BuildErrorMessage("duration must be an integer.")
NEGATIVE_DURATION = BuildErrorMessage("You are not allowed to reduce the end " \
                                        "time.")

# ---- Community Error Messages ---- #
MISSING_COMMUNITYNAME = BuildErrorMessage("Missing communityname")
MISSING_ADD_USERID = BuildErrorMessage("Missing userid to be added")
MISSING_COMMUNITYID = BuildErrorMessage("Missing communityid")
NOT_IN_COMMUNITY = BuildErrorMessage("You need to be in the community first.")
DUPLICATE_MEMBERSHIP = BuildErrorMessage("The member is already in or has " \
                                            "been invited to the community.")
NOT_INVITED = BuildErrorMessage("You have not been invited to join this "\
                                    "community")

# ---- Rating Error Messages ---- #
# Repeat: MISSING_SELLERID
