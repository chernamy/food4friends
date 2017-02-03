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

def BuildItemListMessage(items):
    msg = {
        "items": [item.__dict__ for item in items]
    }
    return json.dumps(msg)

def UnwrapItemListMessage(msg):
    items = json.loads(msg)
    return items["items"]

SUCCESS = BuildInfoMessage("Success")

# ---- Login Request Error Messages ---- #
MISSING_USERID = BuildErrorMessage("Missing userid")
INVALID_CREDENTIALS = BuildErrorMessage("Invalid credentials")
ALREADY_LOGGED_IN = BuildErrorMessage("You're already logged in. Logout first.")
NOT_LOGGED_IN = BuildErrorMessage("You are not logged in.")

# ---- Buy Request Error Messages ---- #
# Repeat: NOT_LOGGED_IN
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
INVALID_DURATION = BuildErrorMessage("Invalid duration field "\
                                        "(must be positive integer)")
INVALID_PRICE = BuildErrorMessage("Invalid price (must be nonnegative decimal)")
