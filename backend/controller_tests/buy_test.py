import unittest
import base_test
import extensions
import json
import login_test
import messages
import user_test

class BuyTest(base_test.BaseTestCase):

    BUY_ROUTE = "/api/v1/buy/"
    CURR_BUY_OFFERS_ROUTE = "/api/v1/buy/current/"

    def testBuyViewRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 3)
        r = self.Get(BuyTest.BUY_ROUTE)
        self.assertEquals(set(messages.UnwrapItemListMessage(r.data)),
                set([extensions.TEST_ITEM1, extensions.TEST_ITEM3,
                        extensions.TEST_ITEM4]))

    def testBuyViewRouteNotLoggedIn(self):
        r = self.Get(BuyTest.BUY_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testBuyPostRouteExists(self):
        r = login_test.LoginTest.LoginAsUser(self, 3)

        # User 2 buys from user 1.
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 1}
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
        r = self.Get(BuyTest.BUY_ROUTE)
        sell_offers = messages.UnwrapItemListMessage(r.data)
        user_offer_data = next(offer for offer in sell_offers if
                                offer.userid == userid)
        return user_offer_data

    def testBuyServings(self):
        login_test.LoginTest.LoginAsUser(self, 3)

        # find how many servings are in the initial sell offer for user 1
        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings

        # buy 2 servings from user 1's sell offer
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)

        after_buy_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        after_buy_servings = after_buy_item.servings

        # check that 2 servings were deducted
        self.assertEqual(initial_servings - 2, after_buy_servings)

    def testBuyAllServings(self):
        login_test.LoginTest.LoginAsUser(self, 3)

        # buy all servings of the item
        item_to_buy = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid,
                "servings": item_to_buy.servings}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)

        # check that the seller no longer has any of that item we just bought
        # for sale.
        r = self.Get(BuyTest.BUY_ROUTE)
        self.assertEquals(set(messages.UnwrapItemListMessage(r.data)), 
                set([extensions.TEST_ITEM3, extensions.TEST_ITEM4]))

    def testBuyRoleChanged(self):
        login_test.LoginTest.LoginAsUser(self, 3)
        item_to_buy = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        # check that the role of user3 has changed
        r = user_test.UserTest.GetUserData(self, extensions.TEST_USER3.userid)
        user = messages.UnwrapUserInfoMessage(r.data)
        self.assertEquals(user.role, "buyer")

    def testBuyBadServings(self):
        login_test.LoginTest.LoginAsUser(self, 3)

        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings

        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 0}
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
        login_test.LoginTest.LoginAsUser(self, 3)

        data = {"sellerid": "whoami?", "buyerid": extensions.TEST_USER3.userid,
                "servings": 5}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.NONEXISTENT_SELLER)

    def testMissingFields(self):
        login_test.LoginTest.LoginAsUser(self, 3)
        r = self.PostJSON(BuyTest.BUY_ROUTE)
        self.assertEqual(r.data, messages.NO_JSON_DATA)

        data = {"buyerid": extensions.TEST_USER3.userid, "servings": 3}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_SELLERID)

        data = {"sellerid": extensions.TEST_USER1.userid, "servings": 3}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_BUYERID)

        data = {"sellerid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER3.userid}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.MISSING_SERVINGS)

    def testOfferExpired(self):
        login_test.LoginTest.LoginAsUser(self, 3)

        data = {"sellerid": extensions.TEST_USER2.userid,
                "buyerid": extensions.TEST_USER3.userid,
                "servings": 4}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.OFFER_EXPIRED)

    def testImproperLogin(self):
        data = {"sellerid": extensions.TEST_USER2.userid,
                "buyerid": extensions.TEST_USER3.userid,
                "servings": 4}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.NOT_LOGGED_IN)

        # Try submitting buy request on behalf of someone else
        login_test.LoginTest.LoginAsUser(self, 3)
        data["buyerid"] = extensions.TEST_USER4.userid
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.BUY_WRONG_USERID)

    def testBuyWrongCommunity(self):
        login_test.LoginTest.LoginAsUser(self, 3)
        initial_item = self.GetSellOfferForUser(extensions.TEST_ITEM1.userid)
        initial_servings = initial_item.servings
        login_test.LoginTest.Logout(self)

        login_test.LoginTest.LoginAsUser(self, 6)

        # buy 2 servings from user 1's sell offer
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER6.userid, "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.NOT_IN_SAME_COMMUNITY)

    def testBuyMultipleTransactions(self):
        login_test.LoginTest.LoginAsUser(self, 3)

        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.SUCCESS)

        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 2}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.INVALID_USER_ROLE)

    def testCurrBuyOffersRoute(self):
        login_test.LoginTest.LoginAsUser(self, 5)
        r = self.Get(BuyTest.CURR_BUY_OFFERS_ROUTE)
        buy_offer = extensions.ItemData.FromDict(extensions.TEST_ITEM1.__dict__)
        buy_offer.servings = extensions.TEST_TRANSACTION1.servings
        self.assertEqual(r.data,
                messages.BuildItemListMessage([buy_offer]))
        login_test.LoginTest.Logout(self)

        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.Get(BuyTest.CURR_BUY_OFFERS_ROUTE)
        self.assertEqual(r.data, messages.BuildItemListMessage([]))

    def testCurrBuyOffersInvalid(self):
        r = self.Get(BuyTest.CURR_BUY_OFFERS_ROUTE)
        self.assertEqual(r.data, messages.NOT_LOGGED_IN)

    def testCurrBuyOffersNoServingsLeft(self):
        login_test.LoginTest.LoginAsUser(self, 3)
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid,
                "servings": extensions.TEST_ITEM1.servings}
        r = self.PostJSON(BuyTest.BUY_ROUTE, data)
        self.assertEqual(r.data, messages.SUCCESS)

        r = self.Get(BuyTest.CURR_BUY_OFFERS_ROUTE)
        buy_offer = extensions.ItemData.FromDict(extensions.TEST_ITEM1.__dict__)
        buy_offer.servings = extensions.TEST_ITEM1.servings
        self.assertEqual(r.data, messages.BuildItemListMessage([buy_offer]))

        login_test.LoginTest.Logout(self)
        login_test.LoginTest.LoginAsUser(self, 5)
        buy_offer = extensions.ItemData.FromDict(extensions.TEST_ITEM1.__dict__)
        buy_offer.servings = extensions.TEST_TRANSACTION1.servings
        self.assertEqual(r.data,
                messages.BuildItemListMessage([buy_offer]))
        login_test.LoginTest.Logout(self)

    def testCurrBuyOffersAfterExpiration(self):
        # artificially insert an incomplete buy offer for expired test item 2
        incomplete_transaction = extensions.TransactionData(
                extensions.TEST_ITEM2.userid, extensions.TEST_USER3.userid, 10)
        extensions.Insert(incomplete_transaction)
        extensions.Update(extensions.TEST_USER3, "role = 'buyer'")

        login_test.LoginTest.LoginAsUser(self, 3)
        # Make sure the buy route doesn't lazily delete the offer data for an
        # item that still has incomplete transactions.
        r = self.Get(BuyTest.BUY_ROUTE)
        r = self.Get(BuyTest.CURR_BUY_OFFERS_ROUTE)
        buy_offer = extensions.ItemData.FromDict(extensions.TEST_ITEM2.__dict__)
        buy_offer.servings = 10
        self.assertEqual(r.data, messages.BuildItemListMessage([buy_offer]))
         

if __name__ == "__main__":
    unittest.main()
