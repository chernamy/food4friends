import unittest
import base_test
import json
import extensions
import messages

class BuyTest(base_test.BaseTestCase):
    
    def testBuyViewRouteExists(self):
        r = self.app.get("/api/v1/buy/")
        self.assertEquals(r.data,
                            messages.BuildItemListMessage(
                            [extensions.TEST_ITEM1, extensions.TEST_ITEM2]))

    def testBuyPostRouteExists(self):

        # User 2 buys from user 1.
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 1}
        r = self.app.post("/api/v1/buy/", data=json.dumps(data),
                            content_type="application/json")
        self.assertEquals(r.data, messages.SUCCESS)

if __name__ == "__main__":
    unittest.main()
