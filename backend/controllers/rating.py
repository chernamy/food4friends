from flask import *
import extensions
import messages

rating = Blueprint("/api/v1/rating/", __name__)


@rating.route("/api/v1/rating/", methods=["GET"])
def ViewRatings():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "sellerid" not in request.json:
        return messages.MISSING_SELLERID, 400

    sellerid = request.json.get("sellerid")
    ratings = extensions.Query(extensions.RatingData,
            [("sellerid", sellerid), ("rating", "pending", "!=")])

    return messages.BuildRatingsListMessage(ratings), 200
    
