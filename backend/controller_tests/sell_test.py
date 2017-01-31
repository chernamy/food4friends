import unittest
import base_test
import extensions
import io
import json
import login_test
import messages

class SellTest(base_test.BaseTestCase):
    
    SELL_ROUTE = "/api/v1/sell/"
    TEST_IMAGE = "testdata/fruit.jpeg"

    def LoginAsUser4(self):
        login_data = {"userid": "user4", "password": "password4"}
        r = self.PostJSON(login_test.LoginTest.LOGIN_ROUTE, login_data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testSellRouteExists(self):
        self.LoginAsUser4()

        data = {"userid": "user4",
                "photo": (io.BytesIO(open(SellTest.TEST_IMAGE, "rb").read()),
                            "photo.jpeg"),
                "servings": 20,
                "duration": 10,
                "price": 10.25,
                "address": "-----",
                "description": "fruit"}
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

if __name__ == "__main__":
    unittest.main()
