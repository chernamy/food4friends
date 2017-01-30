from flask import *
import extensions
import messages

buy = Blueprint("api/v1/buy", __name__)

@buy.route("/api/v1/buy", methods=["GET"])
def api_buy_view():
    item_data = extensions.query_items()
    return messages.BuildItemListMessage(item_data)

@buy.route("/api/v1/buy", methods=["POST"])
def api_buy_purchase():
    pass
