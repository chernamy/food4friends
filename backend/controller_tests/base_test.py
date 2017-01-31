import unittest
import app
import config
import extensions
import json

class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        config.env["db"] = "test"
        extensions.Init()
        app.app.config["SECRET_KEY"] = "12345"
        self.app = app.app.test_client()
 
    def tearDown(self):
        pass

    def GetJSON(self, route, data=None):
        """Gets from the given route.

        Args:
            route: (string) the route to which to submit a GET request (end it
                with a trailing "/")
            data: (dict) the data to post. By default, this is None, which posts
                no json data.
        """
        if data is None:
            return self.app.get(route)
        else:
            return self.app.get(route, data=json.dumps(data),
                                content_type="application/json")

    def PostJSON(self, route, data=None):
        """Posts the given data as JSON to the specified route.

        Args:
            route: (string) the route to which to post (end it with a trailing
                    "/")
            data: (dict) the data to post. By default, this is None, which posts
                    no json data.

        Returns:
            (Response) Contains the data about the server's response.
        """
        if data is None:
            return self.app.post(route)
        else:
            return self.app.post(route, data=json.dumps(data),
                                    content_type="application/json")

    def PostFile(self, route, data):
        """Posts the given image with JSON data to the specified route.

        Args:
            route: (string) the route to which to post (end it with a trailing
                    "/")
            data: (dict) the data with the file to post.
        """
        return self.app.post(route, data=data,
                                content_type="multipart/form-data")
