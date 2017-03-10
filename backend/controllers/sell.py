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

@sell.route("/api/v1/sell", methods=["PUT"])
@sell.route("/api/v1/sell/", methods=["PUT"])
def EditOffer():
    if "userid" not in session:
        return messages.NOT_LOGGED_IN, 403

    if "userid" not in request.form:
        return messages.MISSING_USERID, 400

    userid = request.form.get("userid")
    if userid != session["userid"]:
        return messages.NOT_LOGGED_IN, 403
    
    item_data = extensions.Query(extensions.ItemData, [("userid", userid)])
    if not item_data:
        return messages.NOT_SELLER, 400

    item_data = item_data[0]

    # Validate all data provided by client first
    if "photo" in request.files:
        photo = request.files["photo"]
        ext = photo.filename[(photo.filename.rfind(".")+1):].lower()
        if ext not in ALLOWED_EXT:
            return messages.INVALID_PHOTO_EXT, 400       

    if "servings" in request.form:
        delta_servings = request.form.get("servings")
        try:
            delta_servings = int(delta_servings)
        except:
            return messages.INVALID_DELTA_SERVINGS, 400

        new_servings = item_data.servings + delta_servings
        if new_servings < 0:
            return messages.NEGATIVE_SERVINGS, 400

    if "duration" in request.form:
        delta_duration = request.form.get("duration")
        try:
            delta_duration = int(delta_duration)
        except:
            return messages.INVALID_DELTA_DURATION, 400

        if delta_duration < 0:
            return messages.NEGATIVE_DURATION, 400

    # If all data provided by client was correct, then update it.
    if "photo" in request.files:
        # delete the old photo to save space
        try:
            os.remove(item_data.photo)
        except:
            pass

        # put in the new photo
        photo_path = os.path.join(IMAGE_DIR, userid + "." + ext)
        photo.save(photo_path)
        extensions.Update(item_data, "photo = '%s'" %(photo_path))
        item_data = extensions.Query(extensions.ItemData,
                                        [("userid", userid)])[0]

    if "servings" in request.form:
        new_servings = item_data.servings + delta_servings
        extensions.Update(item_data, "servings = " + str(new_servings))
        item_data = extensions.Query(extensions.ItemData,
                                        [("userid", userid)])[0]

    if "duration" in request.form:
        new_end = item_data.end + delta_duration * 60
        extensions.Update(item_data, "end = " + str(new_end))
        item_data = extensions.Query(extensions.ItemData,
                                        [("userid", userid)])[0]

    if "description" in request.form:
        new_description = request.form.get("description")
        extensions.Update(item_data, "description = '%s'" %(new_description))
    
    return messages.SUCCESS, 200


@sell.route("/api/v1/sell", methods=["POST"])
@sell.route("/api/v1/sell/", methods=["POST"])
def CreateOffer():
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

    user_data = extensions.Query(extensions.UserData, [("userid", userid)])
    if user_data[0].role == "buyer":
        return messages.INVALID_USER_ROLE, 400
    elif user_data[0].role == "seller":
        user_item_data = extensions.Query(extensions.ItemData,
                                            [("userid", userid)])
        curr_time = calendar.timegm(time.gmtime())
        if curr_time >= user_item_data[0].end:
            # user is no longer a seller because the item expired.
            extensions.Delete(user_item_data[0])
            extensions.Update(user_data[0], "role='none'")
            user_data[0].role = "none"
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
    extensions.Insert(new_item)
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
    seller_data = extensions.Query(extensions.UserData, [("userid", userid)])[0]
    if seller_data.role != "seller":
        return messages.NOT_SELLER, 403

    buyerid = request.json.get("buyerid")

    # confirm buyer exists
    buyer_data = extensions.Query(extensions.UserData, [("userid", buyerid)])
    if not buyer_data:
        return messages.NONEXISTENT_BUYER, 400
    buyer_data = buyer_data[0]

    # confirm actually a buyer
    if buyer_data.role != "buyer":
        return messages.NOT_BUYER, 400

    transaction_data = extensions.Query(extensions.TransactionData,
            [("sellerid", userid), ("buyerid", buyerid)])
    if not transaction_data:
        return messages.NONEXISTENT_TRANSACTION, 400

    transaction_data = transaction_data[0]
    extensions.Delete(transaction_data)

    # the buyer goes back to having no role
    extensions.Update(buyer_data, "role='none'")
    buyer_data.role = "none"

    # if the seller has completed all transactions and has no sell offer
    # remaining, then the seller also goes back to having no role
    if (not extensions.Query(extensions.ItemData, [("userid", userid)]) and
        not extensions.Query(extensions.TransactionData,
                                [("sellerid", userid)])):
        extensions.Update(seller_data, "role='none'")
        seller_data.role = "none"
    
    return messages.SUCCESS, 200

