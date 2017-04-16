import os

#"""
env = dict(
    host = "0.0.0.0",
    port = 3000,
    state = "test",
    db_user = "root",
    db_passwd = "root",
    db_name = "test",
    image_dir = os.path.join("static", "images"), 
)
#"""

if "DB_AUTH" in os.environ:
    env["host"] = "%s@us-cdbr-iron-east-03.cleardb.net" %(os.environ["DB_AUTH"])
    db_data = os.environ["DB_AUTH"].split(":")
    env["db_user"] = db_data[0]
    env["db_passwd"] = db_data[1]
    env["db_name"] = "heroku_431332b5e61621b"

