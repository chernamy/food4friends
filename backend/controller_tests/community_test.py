import unittest
import base_test
import extensions
import login_test
import messages

class CommunityTest(base_test.BaseTestCase):

    ALL_COMMUNITIES_ROUTE = "/api/v1/communities/"
    SPECIFIC_COMMUNITY_ROUTE = "/api/v1/community/"

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

        # check that user got added to community
        data = {"communityid": 3}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertEquals(set(messages.UnwrapMembersListMessage(r.data)),
                            set([extensions.TEST_USER1.userid]))

    def testGetCommunityMembersRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"communityid": 1}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertEquals(set(messages.UnwrapMembersListMessage(r.data)),
                            set([extensions.TEST_USER1.userid,
                                    extensions.TEST_USER2.userid,
                                    extensions.TEST_USER3.userid,
                                    extensions.TEST_USER4.userid,
                                    extensions.TEST_USER5.userid]))

    def testGetCommunityMembersRouteInvalid(self):
        data = {"communityid": 1}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        data = {}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_COMMUNITYID)
        

if __name__ == "__main__":
    unittest.main()
