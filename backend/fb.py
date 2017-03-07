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
    APP_TOKEN = f.readline().rstrip("\n")

def GetTestUsers():
    url = UrlFor("accounts/test-users")
    payload = {
        "access_token": APP_TOKEN
    }
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        data = json.loads(r.text)["data"]
        return r.status_code, data
    else:
        return r.status_code, r.text

def VerifyAccessToken(user_id, access_token):
    """Determines if the given access token is valid for the given user.

    Args:
        user_id: (string) A user id.
        access_token: (string) An access token.

    Returns:
        (bool) True if the given access token is valid for the given user. False
            otherwise.
    """
    url = "https://graph.facebook.com/debug_token"
    payload = {
        "input_token": access_token,
        "access_token": APP_TOKEN
    }
    r = requests.get(url, params=payload)
    token_info = json.loads(r.text)["data"]
    if "user_id" in token_info and token_info["user_id"] == user_id:
        return True
    return False

