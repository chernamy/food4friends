from flask import *
import extensions
import json
import messages
import requests

APP_ID = "388599011490992"
FB_GRAPH_URL = "https://graph.facebook.com/v2.8/" + APP_ID

def UrlFor(fb_graph_route):
    return FB_GRAPH_URL + "/" + fb_graph_route

# Make sure the file is in your gitignore.
with open("fb.token") as f:
    FB_TOKEN = f.readline().rstrip("\n")

def GetTestUsers():
    url = UrlFor("accounts/test-users")
    payload = {
        "access_token": FB_TOKEN
    }
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        data = json.loads(r.text)["data"]
        return r.status_code, data
    else:
        return r.status_code, r.text

