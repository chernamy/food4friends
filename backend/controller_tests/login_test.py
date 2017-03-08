import unittest
import base_test
import fb_test
import json
import messages

class LoginTest(base_test.BaseTestCase):

    LOGIN_ROUTE = "/api/v1/login/"
    LOGOUT_ROUTE = "/api/v1/logout/"

    @staticmethod
    def LoginAsUser(test_driver, user_num):
        """Logs in as the given user

        Args:
            test_driver: (BaseTest) instance of a test driver that needs to
                log in.
            user_num: (int) an int 1-5 that is the user to log in.

        Returns:
            r: (Response) The response from the server.
        """
        test_user_data = fb_test.FBTest.GetTestUserData(user_num)
        user_id = test_user_data["id"]
        token = test_user_data["access_token"]
        data = {"userid": user_id, "token": token}
        r = test_driver.PostJSON(LoginTest.LOGIN_ROUTE, data)
        return r

    @staticmethod
    def Logout(test_driver):
        """Logs out

        Args:
            test_driver: (BaseTest) instance of a test driver that needs to
                log out.
        """
        test_driver.PostJSON(LoginTest.LOGOUT_ROUTE)

    def testLoginRouteExists(self):
        r = LoginTest.LoginAsUser(self, 1)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLogoutRouteExists(self):
        LoginTest.LoginAsUser(self, 1)
        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLoginFailed(self):
        data = {"userid": "unknown_user", "token": "wrong token"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_CREDENTIALS)

        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testMissingFields(self):
        data = {}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)

        data = {"userid": "user1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_ACCESS_TOKEN)

    def testMultipleLogin(self):
        LoginTest.LoginAsUser(self, 1)
        r = LoginTest.LoginAsUser(self, 2)
        self.assertEquals(r.data, messages.ALREADY_LOGGED_IN)

if __name__ == "__main__":
    unittest.main()
