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

if __name__ == "__main__":
    unittest.main()
