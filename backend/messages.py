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
    return extensions.UserData(**user_data)

def BuildItemListMessage(items):
    msg = {
        "items": [item.__dict__ for item in items]
    }
    return json.dumps(msg)

def UnwrapItemListMessage(msg):
    items = json.loads(msg)["items"]
    return [extensions.ItemData(**item_dict) for item_dict in items]

SUCCESS = BuildInfoMessage("Success")

# ---- Login Request Error Messages ---- #
MISSING_USERID = BuildErrorMessage("Missing userid")
MISSING_ACCESS_TOKEN = BuildErrorMessage("Missing access token")
INVALID_CREDENTIALS = BuildErrorMessage("Invalid credentials")
ALREADY_LOGGED_IN = BuildErrorMessage("You're already logged in. Logout first.")
NOT_LOGGED_IN = BuildErrorMessage("You are not logged in.")

# ---- User Request Error Messages ---- #
# Repeat: NOT_LOGGED_IN
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

# ---- Sell Request Error Messages ---- #
# Repeat: NOT_LOGGED_IN
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
INVALID_USER_ROLE = BuildErrorMessage("You are already a buyer or seller. " \
                    "Finish that transaction before making a new sell offer.")

# ---- Complete Transaction Error Messages ---- #
# Repeat: NOT_LOGGED_IN
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
