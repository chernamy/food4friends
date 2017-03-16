import unittest
import base_test
import extensions
import login_test
import messages

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
        data = {"sellerid": extensions.TEST_USER1.userid, "rating": 3}
        r = self.PostJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        new_rating = extensions.RatingData.FromDict(
                extensions.TEST_RATING4.__dict__)
        new_rating.rating = "3"
        data = {"sellerid": extensions.TEST_USER1.userid}
        r = self.GetJSON(RatingTest.RATING_ROUTE, data)
        self.assertEquals(r.data, messages.BuildRatingsListMessage([
                            extensions.TEST_RATING1, extensions.TEST_RATING2,
                            extensions.TEST_RATING3, new_rating]))
    
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
