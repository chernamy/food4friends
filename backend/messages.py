from flask import *
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
MISSING_PASSWORD = BuildErrorMessage("Missing password")
INVALID_CREDENTIALS = BuildErrorMessage("Invalid credentials")
NOT_LOGGED_IN = BuildErrorMessage("You are not logged in.")

# ---- Buy Request Error Messages ---- #
MISSING_SELLERID = BuildErrorMessage("Missing sellerid field")
MISSING_BUYERID = BuildErrorMessage("Missing buyerid field")
MISSING_SERVINGS = BuildErrorMessage("Missing servings field")
INVALID_SERVINGS = BuildErrorMessage("Invalid servings field (must be int)")
NONEXISTENT_SELLER = BuildErrorMessage("No sell offer for given sellerid field")
TOO_MANY_SERVINGS = BuildErrorMessage(
                        "Servings field too large for sell offer")
OFFER_EXPIRED = BuildErrorMessage("Offer has already expired")
