import unittest
import base_test
import json
import messages

class LoginTest(base_test.BaseTestCase):

    LOGIN_ROUTE = "/api/v1/login/"
    LOGOUT_ROUTE = "/api/v1/logout/"

    def testLoginRouteExists(self):
        data = {"userid": "user1", "password": "password1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLogoutRouteExists(self):
        data = {"userid": "user1", "password": "password1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLoginFailed(self):
        data = {"userid": "user1", "password": "password2"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_CREDENTIALS)

        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testMissingFields(self):
        data = {"password": "password1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)

        data = {"userid": "user1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_PASSWORD)
        
    def testMultipleLogin(self):
        data = {"userid": "user1", "password": "password1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        data = {"userid": "user2", "password": "password2"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.ALREADY_LOGGED_IN)

if __name__ == "__main__":
    unittest.main()
