import unittest
import base_test
import json
import messages

class LoginTest(base_test.BaseTestCase):

    def testLoginRouteExists(self):
        data = {"username": "username", "password": "password"}
        r = self.app.post("/api/v1/login", data=json.dumps(data),
                            content_type="application/json")
        self.assertEquals(r.data,
                            messages.BuildInfoMessage("Successfully logged in "\
                                                        "as %s" %("username")))

    def testLogoutRouteExists(self):
        data = {"username": "username", "password": "password"}
        r = self.app.post("/api/v1/login", data=json.dumps(data),
                            content_type="application/json")
        self.assertEquals(r.data,
                            messages.BuildInfoMessage("Successfully logged in "\
                                                        "as %s" %("username")))

        r = self.app.post("/api/v1/logout")
        self.assertEquals(r.data,
                            messages.BuildInfoMessage("Successfully logged "\
                                                        "out"))
        

if __name__ == "__main__":
    unittest.main()
