import unittest
import app
import config
import extensions

class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        config.env["db"] = "test"
        extensions.Init()
        app.app.config["SECRET_KEY"] = "12345"
        self.app = app.app.test_client()
 
    def tearDown(self):
        pass
