from flask import *
import calendar
import time
import extensions
import messages

buy = Blueprint("api/v1/buy", __name__)

@buy.route("/api/v1/buy", methods=["GET"])
@buy.route("/api/v1/buy/", methods=["GET"])
def api_buy_view():
    item_data = extensions.QueryItems()
    return messages.BuildItemListMessage(item_data), 200

@buy.route("/api/v1/buy", methods=["POST"])
@buy.route("/api/v1/buy/", methods=["POST"])
def api_buy_purchase():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "sellerid" not in request.json:
        return messages.MISSING_SELLERID, 400
    if "buyerid" not in request.json:
        return messages.MISSING_BUYERID, 400
    if "servings" not in request.json:
        return messages.MISSING_SERVINGS, 400

    sellerid = request.json.get("sellerid")
    buyerid = request.json.get("buyerid")

    if buyerid != session["userid"]:
        return messages.NOT_LOGGED_IN, 403

    try:
        servings = int(request.json.get("servings"))
    except:
        return messages.INVALID_SERVINGS, 400

    if servings <= 0:
        return messages.INVALID_SERVINGS, 400

    item_data = extensions.QueryItems([("userid", sellerid)])
    if not item_data:
        return messages.NONEXISTENT_SELLER, 400

    offer_start = item_data[0].start
    offer_end = offer_start + item_data[0].duration * 60
    curr_time = calendar.timegm(time.gmtime())
    if curr_time > offer_end:
        return messages.OFFER_EXPIRED, 400

    seller_servings = item_data[0].servings
    if servings > seller_servings:
        return messages.TOO_MANY_SERVINGS, 400

    extensions.UpdateItems("servings = servings - %d" %(servings),
                            [("userid", sellerid)])

    # TODO(mjchao): Update database to reflect that buyer has purchased
    # this item.
    return messages.SUCCESS, 200
    
