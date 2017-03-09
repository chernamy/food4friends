import unittest
import app
import config
import extensions
import json

class BaseTestCase(unittest.TestCase):
    
    BASE_HTTP_URL = "http://localhost"
    BASE_HTTPS_URL = "https://localhost"

    def setUp(self):
        config.env["db"] = "test"
        extensions.Init()
        app.app.config["SECRET_KEY"] = "12345"
        app.app.config["SSL"] = True
        self.app = app.app.test_client()
 
    def tearDown(self):
        pass

    def GetJSON(self, route, data=None, https=False):
        """Gets from the given route.

        Args:
            route: (string) the route to which to submit a GET request (end it
                with a trailing "/")
            data: (dict) the data to post. By default, this is None, which posts
                no json data.
            https: (bool) whether to use https (True) or http (False).

        Returns:
            (Response) Contains the data about the server's response.
        """
        base_url = (BaseTestCase.BASE_HTTPS_URL if https
                    else BaseTestCase.BASE_HTTP_URL)
        if data is None:
            return self.app.get(route, base_url=base_url)
        else:
            return self.app.get(route, data=json.dumps(data),
                                content_type="application/json",
                                base_url=base_url)

    def PostJSON(self, route, data=None, https=False):
        """Posts the given data as JSON to the specified route.

        Args:
            route: (string) the route to which to post (end it with a trailing
                    "/")
            data: (dict) the data to post. By default, this is None, which posts
                    no json data.
            https: (bool) whether to use https (True) or http (False).

        Returns:
            (Response) Contains the data about the server's response.
        """
        base_url = (BaseTestCase.BASE_HTTPS_URL if https
                    else BaseTestCase.BASE_HTTP_URL)
        if data is None:
            return self.app.post(route, base_url=base_url)
        else:
            return self.app.post(route, data=json.dumps(data),
                                    content_type="application/json",
                                    base_url=base_url)

    def PostFile(self, route, data, https=False):
        """Posts the given image with JSON data to the specified route.

        Args:
            route: (string) the route to which to post (end it with a trailing
                    "/")
            data: (dict) the data with the file to post.
            https: (bool) whether to use https (True) or http (False).

        Returns:
            (Response) Contains the data about the server's response.
        """
        base_url = (BaseTestCase.BASE_HTTPS_URL if https
                    else BaseTestCase.BASE_HTTP_URL)
        return self.app.post(route, data=data,
                                content_type="multipart/form-data",
                                base_url=base_url)

    def PutFile(self, route, data, https=False):
        """Puts the given image with JSON data to the specified route.

        Args:
            route: (string) the route to which to post (end it with a trailing
                    "/")
            data: (dict) the data with the file to post.
            https: (bool) whether to use https (True) or http (False).

        Returns:
            (Response) Contains the data about the server's response.
        """
        base_url = (BaseTestCase.BASE_HTTPS_URL if https
                    else BaseTestCase.BASE_HTTP_URL)
        return self.app.put(route, data=data,
                            content_type="multipart/form-data",
                            base_url=base_url)

