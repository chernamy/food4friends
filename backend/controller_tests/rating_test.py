import unittest
import base_test
import buy_test
import extensions
import login_test
import messages
import sell_test

class RatingTest(base_test.BaseTestCase):

    RATING_ROUTE = "/api/v1/rating/"

    def testGetRatingsRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"sellerid": extensions.TEST_USER1.userid}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data,
                messages.BuildRatingsListMessage(
                        [extensions.TEST_RATING1,
                            extensions.TEST_RATING2,
                            extensions.TEST_RATING3]))

    def testGetRatingsNoneAvailable(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"sellerid": extensions.TEST_USER2.userid}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.BuildRatingsListMessage([]))

    def testGetRatingsInvalid(self):
        data = {"sellerid": extensions.TEST_USER2.userid}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.GetJSON(RatingTest.RATING_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        data = {}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_SELLERID)

    def testSubmitRatingRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 4)
        data = {"sellerid": extensions.TEST_USER1.userid, "rating": 3,
                "description": "okay"}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        new_rating = extensions.RatingData.FromDict(
                extensions.TEST_RATING4.__dict__)
        new_rating.rating = "3"
        new_rating.description = "okay"
        data = {"sellerid": extensions.TEST_USER1.userid}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.BuildRatingsListMessage([
                            extensions.TEST_RATING1, extensions.TEST_RATING2,
                            extensions.TEST_RATING3, new_rating]))

    def testBuySellRatingProcess(self):
        # User 3 buys from user 7
        login_test.LoginTest.LoginAsUser(self, 3)
        buy_data = {"sellerid": extensions.TEST_USER7.userid,
                    "buyerid": extensions.TEST_USER3.userid,
                    "servings": 10}
        r = self.PostJSON(buy_test.BuyTest.BUY_ROUTE, buy_data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # User 7 completes transaction
        login_test.LoginTest.LoginAsUser(self, 7)
        complete_data = {"userid": extensions.TEST_USER7.userid,
                            "buyerid": extensions.TEST_USER3.userid}
        r = self.PostJSON(sell_test.SellTest.COMPLETE_ROUTE, complete_data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # User 6 submits rating
        login_test.LoginTest.LoginAsUser(self, 3)
        rating_data = {"sellerid": extensions.TEST_USER7.userid, "rating": 5,
                        "description": "fantastic"}
        r = self.PostJSON(RatingTest.RATING_ROUTE, rating_data)
        self.assertEquals(r.data, messages.SUCCESS)

        # Check updated rating
        rating_data = {"sellerid": extensions.TEST_USER7.userid}
        new_rating = extensions.RatingData(5, extensions.TEST_USER7.userid,
                                            extensions.TEST_USER3.userid, "5",
                                            "fantastic")
        r = self.GetJSON(RatingTest.RATING_ROUTE, rating_data)
        self.assertEquals(r.data,
                            messages.BuildRatingsListMessage([new_rating]))

    
    def testSubmitRatingRouteInvalid(self):
        data = {"sellerid": extensions.TEST_USER1.userid, "rating": 3}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 4)
        data = {"sellerid": extensions.TEST_USER1.userid}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_RATING)

        data = {"rating": 3}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_SELLERID) 

        data = {"sellerid": extensions.TEST_USER1.userid, "rating": "invalid"}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.INVALID_RATING)

        data = {"sellerid": extensions.TEST_USER5.userid, "rating": 3}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.NO_RECENT_TRANSACTION)

        data = {"sellerid": "not a user id", "rating": 2}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.NO_RECENT_TRANSACTION)

if __name__ == "__main__":
    unittest.main()
