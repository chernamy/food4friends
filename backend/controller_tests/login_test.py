import unittest
import base_test
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
        """
        data = {"userid": "user%d" %(user_num)}
        r = test_driver.PostJSON(LoginTest.LOGIN_ROUTE, data)

    @staticmethod
    def Logout(test_driver):
        """Logs out

        Args:
            test_driver: (BaseTest) instance of a test driver that needs to
                log out.
        """
        test_driver.PostJSON(LoginTest.LOGOUT_ROUTE)

    def testLoginRouteExists(self):
        data = {"userid": "user1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLogoutRouteExists(self):
        data = {"userid": "user1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.SUCCESS)

    def testLoginFailed(self):
        data = {"userid": "unknown_user"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_CREDENTIALS)

        r = self.PostJSON(LoginTest.LOGOUT_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testMissingFields(self):
        data = {}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)

    def testMultipleLogin(self):
        data = {"userid": "user1"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        data = {"userid": "user2"}
        r = self.PostJSON(LoginTest.LOGIN_ROUTE, data)
        self.assertEquals(r.data, messages.ALREADY_LOGGED_IN)

if __name__ == "__main__":
    unittest.main()
