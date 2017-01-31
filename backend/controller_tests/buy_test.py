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

    def GetSellOfferForUser(self, userid):
        """Gets the sell offer for the given user.

        Args:
            userid: (string) A user's userid.

        Returns:
            item_data: (ItemData) The item data representing the sell offer
                for the specified user.
        """
        r = self.GetJSON(BuyTest.BUY_ROUTE)
        sell_offers = messages.UnwrapItemListMessage(r.data)
        user_offer_data = next(offer for offer in sell_offers if
                                offer["userid"] == userid)
        return extensions.ItemData(**user_offer_data)

    def testBuy2Serving(self):
        # find how many servings are in the initial sell offer for user 1
        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings

        # buy 2 servings from user 1's sell offer
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)

        after_buy_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        after_buy_servings = after_buy_item.servings

        # check that 2 servings were deducted
        self.assertEqual(initial_servings - 2, after_buy_servings)

    def testBuyBadServings(self):
        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings

        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 0}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.INVALID_SERVINGS)

        data["servings"] = -100
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.INVALID_SERVINGS)

        data["servings"] = 99999999
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.TOO_MANY_SERVINGS)
        
        after_buy_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        after_buy_servings = after_buy_item.servings

        # make sure that # of servings did not change
        self.assertEqual(initial_servings, after_buy_servings)

    def testBadSellerId(self):
        data = {"sellerid": "whoami?", "buyerid": "user3", "servings": 5}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.NONEXISTENT_SELLER)

    def testBadBuyerId(self):
        pass

    def testMissingFields(self):
        data = {"buyerid": "user3", "servings": 3}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_SELLERID)

        data = {"sellerid": "user1", "servings": 3}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_BUYERID)

        data = {"sellerid": "user1", "buyerid": "user3"}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_SERVINGS)


if __name__ == "__main__":
    unittest.main()
