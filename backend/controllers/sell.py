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
    if user_data[0].role != "none":
        return messages.INVALID_USER_ROLE

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
