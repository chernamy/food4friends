import unittest
import base_test
import buy_test
import calendar
import config
import extensions
import filecmp
import io
import json
import login_test
import messages
import os
import time
import user_test

class SellTest(base_test.BaseTestCase):
    
    SELL_ROUTE = "/api/v1/sell/"
    TEST_IMAGE_PATH = os.path.join("testdata",
            "%s.jpeg" %(extensions.TEST_USER4.userid))
    TEST_INVALID_IMAGE_EXT_PATH = os.path.join("testdata",
            "%s.blah" %(extensions.TEST_USER4.userid))
    IMAGE_DIR = config.env["image_dir"]

    SELL_UPDATE_ROUTE = "/api/v1/sell/"
    TEST_UPDATE_IMAGE_PATH = os.path.join("testdata",
            "%s.jpg" %(extensions.TEST_USER1.userid))

    COMPLETE_ROUTE = "/api/v1/sell/complete/"

    @staticmethod
    def GetTestItem(end=10):
        """Returns a test item. Note: The end time is set to 10, which is
        10 seconds since the epoch start. You might want to change this.

        Args:
            end: (int) The end time in seconds since epoch. It will default
                to 10.

        Returns:
            (ItemData) An item for testing.
        """
        return extensions.ItemData(extensions.TEST_USER4.userid,
                                    SellTest.TEST_IMAGE_PATH, 20, end,
                                    10.25, "-----", "fruit")

    @staticmethod
    def GetTestUpdateDict(end=10):
        data = {"userid": extensions.TEST_USER1.userid,
                "photo": SellTest.GetImageFile(SellTest.TEST_UPDATE_IMAGE_PATH),
                "servings": "100",
                "duration": "10",
                "description": "cake"}
        return data
        

    @staticmethod
    def GetImageFile(filename):
        """Gets the file data for a given image.

        Returns:
            (Tuple of BytesIO and str) The BytesIO object that can be sent
                to the server and the filename of the file being sent to the
                server.
        """
        return (io.BytesIO(open(filename, "rb").read()), filename)

    @staticmethod
    def ConvertItemToPostDict(item):
        """Converts an item to a dict that can be posted as data to the server.

        Args:
            item: (ItemData) The item to be sent to the server

        Returns:
            (dict) The item's data converted into a dict that can be sent
                to the server.
        """
        d = item.__dict__
        d["photo"] = SellTest.GetImageFile(d["photo"])
        d["duration"] = d["end"]
        del d["end"]
        return d

    @staticmethod
    def AreItemsEqual(item1, item2):
        """Determines if two items are equal. They are equal if their
        properties are all the same except for the end time, which is allowed
        to differ by 10 seconds to account for server lag.

        Args:
            item1: (ItemData) some item data
            item2: (ItemData) some item data

        Returns:
            (bool) If item1 and item2 are equal.
        """
        dict1 = item1.__dict__
        end1 = dict1["end"]
        del dict1["end"]

        dict2 = item2.__dict__
        end2 = dict2["end"]
        del dict2["end"]

        # Two items are equal if they have the same properties and
        # the difference between their end times is less than 10 seconds to
        # account for time it takes to send messages to server.
        return (dict1 == dict2) and (abs(end1 - end2) < 10)

    def GetSellOfferForUser(self, userid):
        """Gets the sell offer for the given user.

        Args:
            userid: (string) A user's userid.

        Returns:
            (ItemData) The item data representing the sell offer for the
                specified user.
        """
        r = self.Get(buy_test.BuyTest.BUY_ROUTE)
        sell_offers = messages.UnwrapItemListMessage(r.data)
        user_offer_data = next(offer for offer in sell_offers if 
                                offer.userid == userid)
        return user_offer_data

    def MakeSellOffer(self, item):
        """Posts a sell offer to the server for the given item. The "end"
        field of the ItemData will be converted to the duration. E.g. if you
        want a duration of 5 minutes, set the "end" field to 5.

        Args:
            item: (ItemData) The item to be posted as a sell offer to the
                server.
        """
        data = SellTest.ConvertItemToPostDict(item)
        return self.PostFile(SellTest.SELL_ROUTE, data)

    def testSellRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 4)

        r = self.MakeSellOffer(SellTest.GetTestItem())
        self.assertEquals(r.data, messages.SUCCESS)

    def testSellRouteUpdatesOffers(self):
        login_test.LoginTest.LoginAsUser(self, 4)

        try:
            os.remove(os.path.join(SellTest.IMAGE_DIR,
                    "%s.jpeg" %(extensions.TEST_USER4.userid)))
        except:
            pass

        r = self.MakeSellOffer(SellTest.GetTestItem())
        self.assertEquals(r.data, messages.SUCCESS)
        approx_end_time = calendar.timegm(time.gmtime()) + 10 * 60

        found_item = self.GetSellOfferForUser(extensions.TEST_USER4.userid)
        expected_item = self.GetTestItem(approx_end_time)
        expected_item.photo = os.path.join(SellTest.IMAGE_DIR,
                "%s.jpeg" %(extensions.TEST_USER4.userid))
        self.assertTrue(SellTest.AreItemsEqual(expected_item, found_item))

        # check that the image was saved to the server
        self.assertTrue(filecmp.cmp(SellTest.TEST_IMAGE_PATH,
                        os.path.join(SellTest.IMAGE_DIR,
                        "%s.jpeg" %(extensions.TEST_USER4.userid))))

    def testSellRouteMissingFields(self):
        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 4)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["userid"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)
         
        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["photo"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_PHOTO)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["photo"] = self.GetImageFile(SellTest.TEST_INVALID_IMAGE_EXT_PATH)
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_PHOTO_EXT)
 
        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["servings"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_SERVINGS)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["servings"] = 10.5
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_SERVINGS)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["servings"] = -100
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_SERVINGS)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["duration"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_DURATION)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["duration"] = -100
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_DURATION)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["duration"] = 10.23
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_DURATION)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["price"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_PRICE)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        data["price"] = -10.23
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_PRICE)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        # too many decimals - only two decimal points allowed for prices.
        data["price"] = 10.23456789
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_PRICE)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["address"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_ADDRESS)

        data = self.ConvertItemToPostDict(self.GetTestItem()) 
        del data["description"]
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_DESCRIPTION)

        # check that invalid fields didn't affect server's ability to
        # process valid sell offers.
        try:
            os.remove(os.path.join(SellTest.IMAGE_DIR,
                                    "%s.jpeg" %(extensions.TEST_USER4.userid)))
        except:
            pass

        r = self.MakeSellOffer(SellTest.GetTestItem())
        self.assertEquals(r.data, messages.SUCCESS)
        approx_end_time = calendar.timegm(time.gmtime()) + 10 * 60

        found_item = self.GetSellOfferForUser(extensions.TEST_USER4.userid)
        expected_item = self.GetTestItem(approx_end_time)
        expected_item.photo = os.path.join(SellTest.IMAGE_DIR,
                "%s.jpeg" %(extensions.TEST_USER4.userid))
        self.assertTrue(SellTest.AreItemsEqual(expected_item, found_item))

        # check that the image was saved to the server
        self.assertTrue(filecmp.cmp(SellTest.TEST_IMAGE_PATH,
                        os.path.join(SellTest.IMAGE_DIR,
                                    "%s.jpeg" %(extensions.TEST_USER4.userid))))

    def testCannotSellBadUser(self):
        login_test.LoginTest.LoginAsUser(self, 1)

        # cannot sell as user 1 because user 1 is already selling
        data = self.ConvertItemToPostDict(self.GetTestItem())
        data["userid"] = extensions.TEST_USER1.userid
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_USER_ROLE)

        # logout from user 1
        login_test.LoginTest.Logout(self)

        # login as user 5
        login_test.LoginTest.LoginAsUser(self, 5)

        # canot sell as user 5 because user 5 is already buying
        data = self.ConvertItemToPostDict(self.GetTestItem())
        data["userid"] = extensions.TEST_USER5.userid
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_USER_ROLE)

        data = self.ConvertItemToPostDict(self.GetTestItem())
        # try making a sell offer on behalf of someone else
        data["userid"] = extensions.TEST_USER4.userid
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testAcknowledgesExpiredSellOffers(self):
        # you should be allowed to create a sell offer as user 2 because
        # the last sell offer already expired.
        login_test.LoginTest.LoginAsUser(self, 2)
        data = self.ConvertItemToPostDict(self.GetTestItem())
        data["userid"] = extensions.TEST_USER2.userid
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        approx_end_time = calendar.timegm(time.gmtime()) + 10 * 60

        found_item = self.GetSellOfferForUser(extensions.TEST_USER2.userid)
        expected_item = self.GetTestItem(approx_end_time)
        expected_item.userid = extensions.TEST_USER2.userid
        expected_item.photo = os.path.join(SellTest.IMAGE_DIR,
                "%s.jpeg" %(extensions.TEST_USER2.userid))
        self.assertTrue(SellTest.AreItemsEqual(expected_item, found_item))

    def testViewIncompleteTransactionsRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.Get(SellTest.COMPLETE_ROUTE)
        self.assertEquals(r.data, messages.BuildTransactionsListMessage(
                [extensions.TEST_TRANSACTION1]))
        login_test.LoginTest.Logout(self)

        # test no transactions
        login_test.LoginTest.LoginAsUser(self, 2)
        r = self.Get(SellTest.COMPLETE_ROUTE)
        self.assertEquals(r.data, messages.BuildTransactionsListMessage([]))
        login_test.LoginTest.Logout(self)

        # test multiple transactions
        # user 3 will now make a buy offer for item 1, so that user 1
        # has two incomplete transactions
        login_test.LoginTest.LoginAsUser(self, 3)
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid, "servings": 5}
        r = self.PostJSON(buy_test.BuyTest.BUY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # user 1 will now ask for his incomplete transactions and there should
        # be two of them
        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.Get(SellTest.COMPLETE_ROUTE)
        transaction_data1 = extensions.TEST_TRANSACTION1
        transaction_data2 = extensions.TransactionData(
                extensions.TEST_USER1.userid, extensions.TEST_USER3.userid, 5)
        self.assertEquals(set(messages.UnwrapTransactionsListMessage(r.data)),
                            set([transaction_data1, transaction_data2]))

    def testViewIncompleteTransactionsRouteInvalid(self):
        r = self.Get(SellTest.COMPLETE_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testCompleteRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)

        # Try completing the transaction where user1 sells to user5
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

    def testCompleteUpdatesBuyerRole(self):
        login_test.LoginTest.LoginAsUser(self, 1)

        # Try completing the transaction where user1 sells to user5
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = user_test.UserTest.GetUserData(self, extensions.TEST_USER5.userid)
        user = messages.UnwrapUserInfoMessage(r.data)
        self.assertEquals(user.role, "none")

    def testCompleteUpdatesSellerRole(self):
        # finish buying all servings for user1's sell offer
        login_test.LoginTest.LoginAsUser(self, 4)
        data = {"sellerid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER4.userid, "servings": 10}
        r = self.PostJSON(buy_test.BuyTest.BUY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # complete all transactions for user1's sell offer
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER4.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        data["buyerid"] = extensions.TEST_USER5.userid
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        # check that roles have been updated
        r = user_test.UserTest.GetUserData(self, extensions.TEST_USER5.userid)
        user = messages.UnwrapUserInfoMessage(r.data)
        self.assertEquals(user.role, "none")

        r = user_test.UserTest.GetUserData(self, extensions.TEST_USER4.userid)
        user = messages.UnwrapUserInfoMessage(r.data)
        self.assertEquals(user.role, "none")

        r = user_test.UserTest.GetUserData(self, extensions.TEST_USER1.userid)
        user = messages.UnwrapUserInfoMessage(r.data)
        self.assertEquals(user.role, "none")

    def testCompleteRouteMissingFields(self):
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.PostJSON(SellTest.COMPLETE_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        del data["userid"]
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)
        data["userid"] = extensions.TEST_USER1.userid

        del data["buyerid"]
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_BUYERID)
        data["buyerid"] = extensions.TEST_USER5.userid

    def testCompleteRouteInvalidFields(self):
        login_test.LoginTest.LoginAsUser(self, 4)
        data = {"userid": extensions.TEST_USER4.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_SELLER)
        login_test.LoginTest.Logout(self)

        login_test.LoginTest.LoginAsUser(self, 1)
        data["userid"] = extensions.TEST_USER1.userid
        data["buyerid"] = "whoami?"
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.NONEXISTENT_BUYER)

        data["userid"] = extensions.TEST_USER1.userid
        data["buyerid"] = extensions.TEST_USER4.userid
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_BUYER)

    def testCompleteRouteNonexistentTransaction(self):
        # Try hitting an invalid transaction between user2 and user5
        # Note this might become invalidated if we change the DB to remove
        # expired sell offers on a non-lazy policy. user2's offer is expired,
        # but because we haven't made a GET for the buyer offers, user2
        # stays as a seller.
        login_test.LoginTest.LoginAsUser(self, 2)
        data = {"userid": extensions.TEST_USER2.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.NONEXISTENT_TRANSACTION)

    def testCompleteRouteDeletesItemDataWithNoMoreServings(self):
        # test old item data gets removed when all servings have been bought
        # and completed
        # first, user 3 buys all the remaining servings from item 1
        login_test.LoginTest.LoginAsUser(self, 3)
        data = {"sellerid": extensions.TEST_ITEM1.userid,
                "buyerid": extensions.TEST_USER3.userid,
                "servings": extensions.TEST_ITEM1.servings}
        r = self.PostJSON(buy_test.BuyTest.BUY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # then user 1 completes all transactions
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER5.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        data = {"userid": extensions.TEST_USER1.userid,
                "buyerid": extensions.TEST_USER3.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        # now that the offer is complete and all transactions finished, the
        # item data should be removed from the database.
        self.assertEquals(len(extensions.Query(extensions.ItemData,
                [("userid", extensions.TEST_USER1.userid)])), 0)

    def testCompleteRouteDeletesExpiredItemData(self):
        # inject an artificial transaction where user 3 bought item 2, which is
        # now expired. Once user 3's transaction is complete, the expired
        # ItemData should be removed
        incomplete_transaction = extensions.TransactionData(
                extensions.TEST_ITEM2.userid, extensions.TEST_USER3.userid, 10)
        extensions.Insert(incomplete_transaction)
        extensions.Update(extensions.TEST_USER3, "role = 'buyer'")

        login_test.LoginTest.LoginAsUser(self, 2)
        data = {"userid": extensions.TEST_USER2.userid,
                "buyerid": extensions.TEST_USER3.userid}
        r = self.PostJSON(SellTest.COMPLETE_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        self.assertEquals(len(extensions.Query(extensions.ItemData,
                [("userid", extensions.TEST_USER2.userid)])), 0)


    def testUpdateRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = self.GetTestUpdateDict() 
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)
        
        # check that the item was updated
        login_test.LoginTest.LoginAsUser(self, 3)
        r = self.Get(buy_test.BuyTest.BUY_ROUTE)
        expected_item = extensions.ItemData.FromDict(
                            extensions.TEST_ITEM1.__dict__)
        expected_item.photo = os.path.join(SellTest.IMAGE_DIR,
                "%s.jpg" %(extensions.TEST_USER1.userid))
        expected_item.servings += 100
        expected_item.end += 10 * 60
        expected_item.description = "cake"
        self.assertEquals(set(messages.UnwrapItemListMessage(r.data)),
                set([expected_item, extensions.TEST_ITEM3,
                        extensions.TEST_ITEM4]))

        # check that file was updated
        self.assertTrue(filecmp.cmp(SellTest.TEST_UPDATE_IMAGE_PATH,
                        os.path.join(SellTest.IMAGE_DIR,
                                    "%s.jpg" %(extensions.TEST_USER1.userid))))

    def testUpdateRouteInvalidFields(self):
        data = SellTest.GetTestUpdateDict()
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)
        data = SellTest.GetTestUpdateDict()
        del data["userid"]
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_USERID)

        # test invalid photo ext
        data = SellTest.GetTestUpdateDict()
        data["photo"] = SellTest.GetImageFile(os.path.join("testdata",
                "%s.blah" %(extensions.TEST_USER4.userid)))
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_PHOTO_EXT)

        # test non-numerical servings
        data = SellTest.GetTestUpdateDict()
        data["servings"] = "not-a-number"
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_DELTA_SERVINGS)

        # test negative servings
        data = SellTest.GetTestUpdateDict()
        data["servings"] = "-11"
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.NEGATIVE_SERVINGS)

        # test non-numerical duration
        data = SellTest.GetTestUpdateDict()
        data["duration"] = "not-a-number"
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_DELTA_DURATION)

        # test negative duration
        data = SellTest.GetTestUpdateDict()
        data["duration"] = -1
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.NEGATIVE_DURATION)
        
    def testSellRouteSQLInjection(self):
        login_test.LoginTest.LoginAsUser(self, 4)
        sell_item = SellTest.GetTestItem()
        sell_item.description = "; DROP TABLE ITEM;"
        data = self.ConvertItemToPostDict(sell_item)
        r = self.PostFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        # should raise exception if item table was dropped
        found_item = self.GetSellOfferForUser(extensions.TEST_USER4.userid)
        self.assertEquals(found_item.description, sell_item.description)

        login_test.LoginTest.Logout(self)
        login_test.LoginTest.LoginAsUser(self, 1)

        data = SellTest.GetTestUpdateDict()
        data["description"] = "; DROP TABLE ITEM;"
        r = self.PutFile(SellTest.SELL_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        # should raise exception if item table was dropped
        found_item = self.GetSellOfferForUser(extensions.TEST_USER1.userid)
        self.assertEquals(found_item.description, data["description"])

if __name__ == "__main__":
    unittest.main()
