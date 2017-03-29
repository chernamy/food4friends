import unittest
import base_test
import extensions
import json
import login_test
import messages

class UserTest(base_test.BaseTestCase):
    
    USER_ROUTE = "/api/v1/user/"

    @staticmethod
    def GetUserData(test_driver, userid):
        """Gets the user data for the given user.

        Args:
            test_driver: (BaseTest) An instance of a test driver.
            userid: (string) The user id of the user for which information is
                requested.

        Returns:
            (string) The JSON returned by the server.
        """
        data = {"userid": userid}
        return test_driver.Get(UserTest.USER_ROUTE, data)

    def testUserRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER1.userid}
        r = self.Get(UserTest.USER_ROUTE, data)
        self.assertEquals(r.data,
            messages.BuildUserInfoMessage(extensions.TEST_USER1))

    def testUserRouteMissingFields(self):
        data = {"userid": extensions.TEST_USER1.userid}
        r = self.Get(UserTest.USER_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)

        r = self.Get(UserTest.USER_ROUTE)
        self.assertEquals(r.data, messages.NO_URL_PARAMETERS)

if __name__ == "__main__":
    unittest.main()
