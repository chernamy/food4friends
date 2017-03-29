from flask import *
import extensions
import messages

rating = Blueprint("/api/v1/rating/", __name__)


@rating.route("/api/v1/rating/", methods=["GET"])
def ViewRatings():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "sellerid" not in request.args:
        return messages.MISSING_SELLERID, 400

    sellerid = request.args.get("sellerid")
    ratings = extensions.Query(extensions.RatingData,
            [("sellerid", sellerid), ("rating", "pending", "!=")])

    return messages.BuildRatingsListMessage(ratings), 200

@rating.route("/api/v1/rating/pending/", methods=["GET"])
def GetYourPendingRatings():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    pending_ratings = extensions.Query(extensions.RatingData,
                                        [("buyerid", session["userid"]),
                                        ("rating", "pending")])
    return messages.BuildPendingRatingsListMessage(pending_ratings)
    
ALLOWED_RATINGS = set([1, 2, 3, 4, 5])

@rating.route("/api/v1/rating/", methods=["POST"])
def SubmitRating():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if request.json is None:
        return messages.NO_JSON_DATA, 400

    if "sellerid" not in request.json:
        return messages.MISSING_SELLERID, 400

    buyerid = session["userid"]

    if "rating" not in request.json:
        return messages.MISSING_RATING, 400

    sellerid = request.json.get("sellerid")
    rating = request.json.get("rating")
    try:
        rating = int(rating)
    except:
        return messages.INVALID_RATING, 400

    if rating not in ALLOWED_RATINGS:
        return messages.INVALID_RATING, 400

    description = ("" if "description" not in request.json else
                    request.json.get("description"))

    rating_to_submit = extensions.Query(extensions.RatingData,
                                        [("sellerid", sellerid),
                                            ("buyerid", buyerid),
                                            ("rating", "pending")])
    if not rating_to_submit: 
        return messages.NO_RECENT_TRANSACTION, 403

    rating_to_submit = rating_to_submit[0]
    extensions.Update(rating_to_submit, "rating='%d', description='%s'"
                        %(rating, description))
    return messages.SUCCESS, 200

