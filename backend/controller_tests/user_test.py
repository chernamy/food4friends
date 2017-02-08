import unittest
import base_test
import extensions
import json
import login_test
import messages

class UserTest(base_test.BaseTestCase):
    
    USER_ROUTE = "/api/v1/user/"

    def testUserRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": "user1"}
        r = self.GetJSON(UserTest.USER_ROUTE, data)
        self.assertEquals(r.data,
            messages.BuildUserInfoMessage(extensions.TEST_USER1))

if __name__ == "__main__":
    unittest.main()
