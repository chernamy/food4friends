import unittest
import fb

class FBTest(unittest.TestCase):

    def testGetTestUsers(self):
        status_code, data = fb.GetTestUsers()
        self.assertEqual(status_code, 200)

    def testVerifyAccessToken(self):
        _, data = fb.GetTestUsers()
        test_user = data[0]
        user_id = test_user["id"]
        access_token = test_user["access_token"]
        self.assertTrue(fb.VerifyAccessToken(user_id, access_token))
        access_token = "Wrong access token"
        self.assertFalse(fb.VerifyAccessToken(user_id, access_token))

if __name__ == "__main__":
    unittest.main()
