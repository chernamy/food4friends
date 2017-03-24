import os

env = dict(
    host = "0.0.0.0",
    port = 3000,
    state = "test",
    db_user = "root",
    db_passwd = "root",
    image_dir = os.path.join("static", "images"), 
)
