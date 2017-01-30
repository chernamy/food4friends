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

# ---- Buy Request Error Messages ---- #
MISSING_SELLER_ID = BuildErrorMessage("Missing sellerid field")
MISSING_BUYER_ID = BuildErrorMessage("Missing buyerid field")
MISSING_SERVINGS = BuildErrorMessage("Missing servings field")
INVALID_SERVINGS = BuildErrorMessage("Invalid servings field (must be int)")
NONEXISTENT_SELLER = BuildErrorMessage("No sell offer for given sellerid field")
TOO_MANY_SERVINGS = BuildErrorMessage("Servings field too large for sell offer")
