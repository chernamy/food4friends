import unittest
import app
import test_config
import json

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
    
    def testLoginRouteExists(self):
        data = {"username": "user", "password": "password"}
        r = self.app.post("/api/v1/login", data=json.dumps(data))
        self.assertEquals(r.data, "You reached the test login route.")
        

if __name__ == "__main__":
    unittest.main()
