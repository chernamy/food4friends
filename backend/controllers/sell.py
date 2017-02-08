from flask import *
import calendar
import config
import extensions
import messages
import os
import time

sell = Blueprint("/api/v1/sell/", __name__)

ALLOWED_EXT = set(["png", "jpg", "jpeg", "gif"])
IMAGE_DIR = config.env["image_dir"]

@sell.route("/api/v1/sell", methods=["POST"])
@sell.route("/api/v1/sell/", methods=["POST"])
def PostOffer():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "userid" not in request.form:
        return messages.MISSING_USERID, 400
    if "photo" not in request.files:
        return messages.MISSING_PHOTO, 400
    if "servings" not in request.form:
        return messages.MISSING_SERVINGS, 400
    if "duration" not in request.form:
        return messages.MISSING_DURATION, 400
    if "price" not in request.form:
        return messages.MISSING_PRICE, 400
    if "address" not in request.form:
        return messages.MISSING_ADDRESS, 400
    if "description" not in request.form:
        return messages.MISSING_DESCRIPTION, 400

    userid = request.form.get("userid")
    if userid != session["userid"]:
        return messages.NOT_LOGGED_IN, 403

    user_data = extensions.QueryUsers([("userid", userid)])
    if user_data[0].role == "buyer":
        return messages.INVALID_USER_ROLE, 400
    elif user_data[0].role == "seller":
        user_item_data = extensions.QueryItems([("userid", userid)])
        curr_time = calendar.timegm(time.gmtime())
        if curr_time >= user_item_data[0].end:
            # user is no longer a seller because the item expired.
            extensions.DeleteItem(user_item_data[0])
            extensions.UpdateUserRole(user_data[0], "none")
        else:
            return messages.INVALID_USER_ROLE, 400

    photo = request.files["photo"]
    ext = photo.filename[(photo.filename.rfind(".")+1):].lower()
    if ext not in ALLOWED_EXT:
        return messages.INVALID_PHOTO_EXT, 400

    try:
        servings = int(request.form.get("servings"))
    except:
        return messages.INVALID_SERVINGS, 400

    if servings <= 0:
        return messages.INVALID_SERVINGS, 400

    try:
        duration = int(request.form.get("duration"))
    except:
        return messages.INVALID_DURATION, 400

    if duration <= 0:
        return messages.INVALID_DURATION, 400

    try:
        price = float(request.form.get("price"))
    except:
        return messages.INVALID_PRICE, 400

    if price < 0.0:
        return messages.INVALID_PRICE, 400

    # check if there are more than 2 digits after the decimal place
    if round(price, 2) != price:
        return messages.INVALID_PRICE, 400

    address = request.form.get("address")
    description = request.form.get("description")

    photo_path = os.path.join(IMAGE_DIR, userid + "." + ext)
    photo.save(photo_path)

    end = calendar.timegm(time.gmtime()) + duration * 60

    new_item = extensions.ItemData(userid, photo_path, servings, end,
                                    price, address, description)
    extensions.AddItem(new_item)
    return messages.SUCCESS, 200

@sell.route("/api/v1/sell/complete", methods=["POST"])
@sell.route("/api/v1/sell/complete/", methods=["POST"])
def CompleteTransaction():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "userid" not in request.json:
        return messages.MISSING_USERID
    if "buyerid" not in request.json:
        return messages.MISSING_BUYERID

    userid = request.json.get("userid")

    if userid != session["userid"]:
        return messages.NOT_LOGGED_IN, 403

    # confirm actually a seller
    seller_data = extensions.QueryUsers([("userid", userid)])[0]
    if seller_data.role != "seller":
        return messages.NOT_SELLER, 403

    buyerid = request.json.get("buyerid")

    # confirm buyer exists
    buyer_data = extensions.QueryUsers([("userid", buyerid)])
    if not buyer_data:
        return messages.NONEXISTENT_BUYER, 400
    buyer_data = buyer_data[0]

    # confirm actually a buyer
    if buyer_data.role != "buyer":
        return messages.NOT_BUYER, 400

    transaction_data = extensions.QueryTransactions([("sellerid", userid),
                                                        ("buyerid", buyerid)])
    if not transaction_data:
        return messages.NONEXISTENT_TRANSACTION

    transaction_data = transaction_data[0]
    extensions.CompleteTransaction(transaction_data)

    # the buyer goes back to having no role
    extensions.UpdateUserRole(buyer_data, "none")

    # if the seller has completed all transactions and has no sell offer
    # remaining, then the seller also goes back to having no role
    if (not extensions.QueryItems([("userid", userid)]) and
        not extensions.QueryTransactions([("sellerid", userid)])):
        extensions.UpdateUserRole(seller_data, "none")
    
    return messages.SUCCESS, 200
    
    

