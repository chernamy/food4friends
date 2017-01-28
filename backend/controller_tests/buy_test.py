import unittest
import base_test
import json
import extensions
import messages

class BuyTest(base_test.BaseTestCase):
    
    def testBuyViewRouteExists(self):
        r = self.app.get("/api/v1/buy")
        self.assertEquals(r.data,
                            messages.BuildItemListMessage(
                            [extensions.TEST_ITEM1, extensions.TEST_ITEM2]))
        print r.data

if __name__ == "__main__":
    unittest.main()
