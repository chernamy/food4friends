import unittest
import fb
import json
import requests

class FBTest(unittest.TestCase):

    TEST_USER_IDS = ["106477066550909", "114360749093811", "116914598837407",
                        "121248135069937", "166392330540730", "115614082302215",
                        "103294363539139", "100142490522610", "108998629637466",
                        "105305656677266"]

    @staticmethod
    def GetTestUsers():
        url = fb.UrlFor("accounts/test-users")
        payload = {
            "access_token": fb.APP_TOKEN
        }
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            data = json.loads(r.text)["data"]
            return r.status_code, data
        else:
            return r.status_code, r.text


    @staticmethod
    def GetTestUserData(user_num):
        if not (1 <= user_num and user_num <= len(FBTest.TEST_USER_IDS)):
            raise ValueError("There are only %d test users numbered 1..%d"
                                %(len(FBTest.TEST_USER_IDS),
                                    len(FBTest.TEST_USER_IDS)))

        _, user_data = FBTest.GetTestUsers()
        for user in user_data:
            if user["id"] == FBTest.TEST_USER_IDS[user_num - 1]:
                return user


    def testVerifyAccessToken(self):
        test_user = FBTest.GetTestUserData(1)
        user_id = test_user["id"]
        access_token = test_user["access_token"]
        self.assertTrue(fb.VerifyAccessToken(user_id, access_token))
        access_token = "Wrong access token"
        self.assertFalse(fb.VerifyAccessToken(user_id, access_token))


if __name__ == "__main__":
    unittest.main()
