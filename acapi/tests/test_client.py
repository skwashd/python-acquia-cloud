import os
import requests
import requests_mock
import unittest

from .. import Client

@requests_mock.Mocker()
class TestClient(unittest.TestCase):
    """Tests the Acquia Cloud API client class."""

    req = None

    """
        def setup(self, ):
            " ""
            Set up the tests with the mock requests handler.
            " ""
            session = requests.Session()
            adapter = requests_mock.Adapter()
            session.mount('mock', adapter)
    """

    def test_find_credentials(self, m):
        """
        Tests finding the credentials in environment variables
        """
        os.environ['ACQUIA_CLOUD_API_USER'] = 'user'
        os.environ['ACQUIA_CLOUD_API_TOKEN'] = 'token'
        client = Client(cache=None)
        (user, token) = client._Client__find_credentials()
        self.assertEqual(user, 'user')
        self.assertEqual(token, 'token')

    def test_user(self, m):
        email = 'user@example.com'
        m.register_uri('GET',
                       'https://cloudapi.acquia.com/v1/me.json',
                       json={"authenticated_as": email}
                      )
        client = Client(email, 'token')
        user = client.user().get()
        self.assertEqual(user['authenticated_as'], email)

if __name__ == '__main__':
    unittest.main()
