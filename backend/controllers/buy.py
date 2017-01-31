from flask import *
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
    if "sellerid" not in request.json:
        return messages.MISSING_SELLERID, 400
    if "buyerid" not in request.json:
        return messages.MISSING_BUYERID, 400
    if "servings" not in request.json:
        return messages.MISSING_SERVINGS, 400

    sellerid = request.json.get("sellerid")
    buyerid = request.json.get("buyerid")

    buyer_data = extensions.QueryUsers([("userid", buyerid)])
    if not buyer_data:
        return messages.NONEXISTENT_BUYER, 400

    try:
        servings = int(request.json.get("servings"))
    except:
        return messages.INVALID_SERVINGS, 400

    if servings <= 0:
        return messages.INVALID_SERVINGS, 400

    user_data = extensions.QueryItems([("userid", sellerid)])
    if not user_data:
        return messages.NONEXISTENT_SELLER, 400

    seller_servings = user_data[0].servings
    if servings > seller_servings:
        return messages.TOO_MANY_SERVINGS, 400

    extensions.UpdateItems("servings = servings - %d" %(servings),
                            [("userid", sellerid)])
    return messages.SUCCESS, 200
    
