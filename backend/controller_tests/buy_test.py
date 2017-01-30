import unittest
import base_test
import json
import extensions
import messages

class BuyTest(base_test.BaseTestCase):

    BUY_ROUTE = "/api/v1/buy/"
    
    def testBuyViewRouteExists(self):
        r = self.GetJSON(BuyTest.BUY_ROUTE)
        self.assertEquals(r.data,
                            messages.BuildItemListMessage(
                            [extensions.TEST_ITEM1, extensions.TEST_ITEM2]))

    def testBuyPostRouteExists(self):

        # User 2 buys from user 1.
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 1}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testBuy1Serving(self):
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 1}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)


if __name__ == "__main__":
    unittest.main()
