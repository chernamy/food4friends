from flask import *
import calendar
import community
import extensions
import messages
import time

buy = Blueprint("/api/v1/buy", __name__)

@buy.route("/api/v1/buy", methods=["GET"])
@buy.route("/api/v1/buy/", methods=["GET"])
def ViewBuyList():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    item_data = extensions.Query(extensions.ItemData)
    curr_time = calendar.timegm(time.gmtime())
    unexpired_items = []
    for item in item_data:
        if curr_time > item.end:
            extensions.Delete(item)
            user = extensions.Query(extensions.UserData,
                                    [("userid", item.userid)])[0]
            extensions.Update(user, "role='none'")
            user.role = "none"
        else:
            buyerid = session["userid"]
            sellerid = item.userid
            if community.InSameCommunity(buyerid, sellerid):
                unexpired_items.append(item)

    return messages.BuildItemListMessage(unexpired_items), 200

@buy.route("/api/v1/buy", methods=["POST"])
@buy.route("/api/v1/buy/", methods=["POST"])
def Purchase():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "sellerid" not in request.json:
        return messages.MISSING_SELLERID, 400
    if "buyerid" not in request.json:
        return messages.MISSING_BUYERID, 400
    if "servings" not in request.json:
        return messages.MISSING_SERVINGS, 400

    sellerid = request.json.get("sellerid")
    buyerid = request.json.get("buyerid")

    if buyerid != session["userid"]:
        return messages.BUY_WRONG_USERID, 403

    try:
        servings = int(request.json.get("servings"))
    except:
        return messages.INVALID_SERVINGS, 400

    if servings <= 0:
        return messages.INVALID_SERVINGS, 400

    item_data = extensions.Query(extensions.ItemData, [("userid", sellerid)])
    if not item_data:
        return messages.NONEXISTENT_SELLER, 400
    item_data = item_data[0]

    offer_end = item_data.end
    curr_time = calendar.timegm(time.gmtime())
    if curr_time > offer_end:
        return messages.OFFER_EXPIRED, 400

    seller_servings = item_data.servings
    if servings > seller_servings:
        return messages.TOO_MANY_SERVINGS, 400
    
    if servings == seller_servings:
        extensions.Delete(item_data)
    else:
        extensions.Update(item_data, "servings = servings - %d" %(servings))

    if not community.InSameCommunity(buyerid, sellerid):
        return messages.NOT_IN_SAME_COMMUNITY, 403

    # guaranteed to exist because logged in with buyerid
    user_data = extensions.Query(extensions.UserData, [("userid", buyerid)])[0]
    extensions.Update(user_data, "role='buyer'")
    user_data.role = "buyer"

    # add in the transaction data
    transaction = extensions.TransactionData(sellerid, buyerid, servings)
    extensions.Insert(transaction)
    return messages.SUCCESS, 200
    
