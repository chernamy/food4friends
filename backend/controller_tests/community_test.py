import unittest
import base_test
import extensions
import login_test
import messages

class CommunityTest(base_test.BaseTestCase):

    ALL_COMMUNITIES_ROUTE = "/api/v1/communities/"
    JOINED_COMMUNITIES_ROUTE = "/api/v1/communities/joined/"
    INVITED_COMMUNITIES_ROUTE = "/api/v1/communities/invites/"
    SPECIFIC_COMMUNITY_ROUTE = "/api/v1/community/"
    ADD_MEMBER_ROUTE ="/api/v1/community/add/"
    ACCEPT_INVITATION_ROUTE = "/api/v1/community/join/"
    LEAVE_COMMUNITY_ROUTE = "/api/v1/community/leave/"

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

    def testCreateCommunityInvalidRequest(self):
        # test not logged in
        data = {"communityname": "TestCommunity3"}
        r = self.PostJSON(CommunityTest.ALL_COMMUNITIES_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)

        # test missing json
        r = self.PostJSON(CommunityTest.ALL_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        # test missing community name
        data = {}
        r = self.PostJSON(CommunityTest.ALL_COMMUNITIES_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_COMMUNITYNAME)

    def testGetJoinedCommunitiesRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.GetJSON(CommunityTest.JOINED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage(
                [extensions.TEST_COMMUNITY1]))

    def testGetJoinedCommunitiesRouteNoCommunities(self):
        login_test.LoginTest.LoginAsUser(self, 6)
        r = self.GetJSON(CommunityTest.JOINED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage([]))

    def testGetJoinedCommunitiesRouteInvalidRequest(self):
        # test not logged in
        r = self.GetJSON(CommunityTest.JOINED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

    def testGetInvitedCommunitiesRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        login_test.LoginTest.Logout(self)
        login_test.LoginTest.LoginAsUser(self, 6)
        r = self.GetJSON(CommunityTest.INVITED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage(
                [extensions.TEST_COMMUNITY1]))

    def testGetInvitedCommunitiesRouteNoCommunities(self):
        login_test.LoginTest.LoginAsUser(self, 6)
        r = self.GetJSON(CommunityTest.INVITED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage([]))

    def testGetUsersInCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"communityid": 1}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertEquals(set(messages.UnwrapMembersListMessage(r.data)),
                            set([extensions.TEST_USER1.userid,
                                    extensions.TEST_USER2.userid,
                                    extensions.TEST_USER3.userid,
                                    extensions.TEST_USER4.userid,
                                    extensions.TEST_USER5.userid,
                                    extensions.TEST_USER7.userid,
                                    extensions.TEST_USER8.userid,
                                    extensions.TEST_USER9.userid]))

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
        
    def testAddUserToCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        login_test.LoginTest.Logout(self)
        login_test.LoginTest.LoginAsUser(self, 6)
        r = self.GetJSON(CommunityTest.INVITED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data,
            messages.BuildCommunityListMessage([extensions.TEST_COMMUNITY1]))

    def testAddUserToCommunityRouteInvalid(self):
        # test not logged in
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)

        # test no json
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        # test missing userid
        data = {"communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_ADD_USERID)

        # test missing communityid
        data = {"userid": extensions.TEST_USER6.userid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_COMMUNITYID)

        # test not in community
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY2.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_IN_COMMUNITY)

        # test duplicate membership
        data = {"userid": extensions.TEST_USER2.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.DUPLICATE_MEMBERSHIP)

    def testJoinCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        login_test.LoginTest.Logout(self)
        login_test.LoginTest.LoginAsUser(self, 6)
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = self.GetJSON(CommunityTest.JOINED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage(
                [extensions.TEST_COMMUNITY1]))

        data = {"communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.GetJSON(CommunityTest.SPECIFIC_COMMUNITY_ROUTE, data)
        self.assertTrue(extensions.TEST_USER6.userid in
                        set(messages.UnwrapMembersListMessage(r.data)))

    def testJoinCommunityRouteInvalidRequest(self):
        # first, invite user 6 to join the community
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"userid": extensions.TEST_USER6.userid,
                "communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ADD_MEMBER_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)
        login_test.LoginTest.Logout(self)

        # test not logged in
        data = {"communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 6)

        # test no json
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

        # test missing communityid
        data = {}
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE, data)
        self.assertEquals(r.data, messages.MISSING_COMMUNITYID)

        # test not invited
        data = {"communityid": extensions.TEST_COMMUNITY2.communityid}
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_INVITED)

        # test try to join nonexistent community
        data = {"communityid": 1000}
        r = self.PostJSON(CommunityTest.ACCEPT_INVITATION_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_INVITED)

    def testLeaveCommunityRouteExists(self):
        login_test.LoginTest.LoginAsUser(self, 1)
        data = {"communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.DeleteJSON(CommunityTest.LEAVE_COMMUNITY_ROUTE, data)
        self.assertEquals(r.data, messages.SUCCESS)

        r = self.GetJSON(CommunityTest.JOINED_COMMUNITIES_ROUTE)
        self.assertEquals(r.data, messages.BuildCommunityListMessage([]))

    def testLeaveCommunityRouteMissingFields(self):
        data = {"communityid": extensions.TEST_COMMUNITY1.communityid}
        r = self.DeleteJSON(CommunityTest.LEAVE_COMMUNITY_ROUTE, data)
        self.assertEquals(r.data, messages.NOT_LOGGED_IN)

        login_test.LoginTest.LoginAsUser(self, 1)
        r = self.DeleteJSON(CommunityTest.LEAVE_COMMUNITY_ROUTE)
        self.assertEquals(r.data, messages.NO_JSON_DATA)

if __name__ == "__main__":
    unittest.main()
