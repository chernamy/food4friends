from flask import *
import extensions
import messages

buy = Blueprint("api/v1/buy", __name__)

@buy.route("/api/v1/buy", methods=["GET"])
@buy.route("/api/v1/buy/", methods=["GET"])
def api_buy_view():
    item_data = extensions.query_items()
    return messages.BuildItemListMessage(item_data)

@buy.route("/api/v1/buy", methods=["POST"])
@buy.route("/api/v1/buy/", methods=["POST"])
def api_buy_purchase():
    if "sellerid" not in request.json:
        return messages.MISSING_SELLER_ID
    if "buyerid" not in request.json:
        return messages.MISSING_BUYER_ID
    if "servings" not in request.json:
        return messages.MISSING_SERVINGS

    sellerid = request.json.get("sellerid")
    buyerid = request.json.get("buyerid")
    try:
        servings = int(request.json.get("servings"))
    except:
        return messages.INVALID_SERVINGS

    user_data = extensions.query_items([("userid", sellerid)])
    if not user_data:
        return messages.NONEXISTENT_SELLER

    seller_servings = user_data[0].servings
    if servings > seller_servings:
        return messages.TOO_MANY_SERVINGS

    #TODO update servings
    print "Success"
    return messages.SUCCESS
    
