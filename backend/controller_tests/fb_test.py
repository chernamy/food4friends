import unittest
import fb

class FBTest(unittest.TestCase):

    def testGetTestUsers(self):
        status_code, data = fb.GetTestUsers()
        self.assertEqual(status_code, 200)

if __name__ == "__main__":
    unittest.main()
