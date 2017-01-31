from flask import *
import calendar
import time
import extensions
import messages

sell = Blueprint("/api/v1/sell/", __name__)

@sell.route("/api/v1/sell", methods=["POST"])
@sell.route("/api/v1/sell/", methods=["POST"])
def api_sell_post():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    return messages.SUCCESS, 200
