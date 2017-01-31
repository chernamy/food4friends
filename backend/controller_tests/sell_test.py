import unittest
import base_test
import extensions
import json
import login_test
import messages

class SellTest(base_test.BaseTestCase):
    
    SELL_ROUTE = "/api/v1/sell/"

    def LoginAsUser4(self):
        login_data = {"userid": "user4", "password": "password4"}
        r = self.PostJSON(login_test.LoginTest.LOGIN_ROUTE, login_data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testSellRouteExists(self):
        self.LoginAsUser4()
        r = self.PostJSON(SellTest.SELL_ROUTE)
        self.assertEquals(r.data, messages.SUCCESS)

if __name__ == "__main__":
    unittest.main()
