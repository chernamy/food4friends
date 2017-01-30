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

    def testBuy1Serving(self):
        # find how many servings are in the initial sell offer for user 1
        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings
        print "Initial servings:", initial_servings

        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": "user3", "servings": 1}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)

        after_buy_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        after_buy_servings = after_buy_item.servings
        print "After servings:", after_buy_servings


if __name__ == "__main__":
    unittest.main()
