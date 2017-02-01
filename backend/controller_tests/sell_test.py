import unittest
import base_test
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

class SellTest(base_test.BaseTestCase):
    
    SELL_ROUTE = "/api/v1/sell/"
    TEST_IMAGE_PATH = "testdata/user4.jpeg"
    IMAGE_DIR = config.env["image_dir"]

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
        return extensions.ItemData("user4", SellTest.TEST_IMAGE_PATH, 20, end,
                                    10.25, "-----", "fruit")

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
        r = self.GetJSON(BuyTest.BUY_ROUTE)
        sell_offers = messages.UnwrapItemListMessage(r.data)
        user_offer_data = next(offer for offer in sell_offers if 
                                offer["userid"] == userif)
        return extensions.ItemData(**user_offer_data)

    def LoginAsUser4(self):
        """Logs in as user4.
        """
        login_data = {"userid": "user4", "password": "password4"}
        r = self.PostJSON(login_test.LoginTest.LOGIN_ROUTE, login_data)
        self.assertEquals(r.data, messages.SUCCESS)

    def MakeSellOffer(self, item):
        """Posts a sell offer to the server for the given item.

        Args:
            item: (ItemData) The item to be posted as a sell offer to the
                server.
        """
        data = SellTest.ConvertItemToPostDict(item)
        return self.PostFile(SellTest.SELL_ROUTE, data)

    def testSellRouteExists(self):
        self.LoginAsUser4()

        r = self.MakeSellOffer(SellTest.GetTestItem())
        self.assertEquals(r.data, messages.SUCCESS)

    def testSellRouteUpdatesOffers(self):
        return
        self.LoginAsUser4()

        try:
            os.remove(os.path.join(SellTest.IMAGE_DIR, "user4.jpeg"))
        except:
            pass

        r = self.MakeSellOffer(SellTest.GetTestItem())
        self.assertEquals(r.data, messages.SUCCESS)
        approx_end_time = calendar.timegm(time.gmtime()) + 10 * 60

        found_item = self.GetOfferForUser("user4")
        expected_item = self.GetTestItem(approx_end_time)
        self.assertTrue(SellTest.AreItemsEqual(expected_item, found_item))

        # check that the image was saved to the server
        self.assertTrue(filecmp.cmp(SellTest.TEST_IMAGE_PATH,
                        os.path.join(SellTest.IMAGE_DIR, "user4.jpeg")))
        
    

if __name__ == "__main__":
    unittest.main()
