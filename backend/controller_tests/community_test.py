import unittest
import base_test
import extensions
import login_test
import messages

class CommunityTest(base_test.BaseTestCase):

    ALL_COMMUNITIES_ROUTE = "/api/v1/communities/"

    def testViewCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.GetJSON(CommunityTest.ALL_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage(
                [extensions.TEST_COMMUNITY1, extensions.TEST_COMMUNITY2]))

    def testViewCommunityNotLoggedIn(self):
        r = self.GetJSON(CommunityTest.ALL_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testCreateCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)

        data = {"communityname": "TestCommunity3"}
        r = self.PostJSON(CommunityTest.ALL_COMMUNITIES_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = self.GetJSON(CommunityTest.ALL_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage(
                [extensions.TEST_COMMUNITY1, extensions.TEST_COMMUNITY2,
                    extensions.CommunityData(3, "TestCommunity3")]))
        

if __name__ == "__main__":
    unittest.main()
