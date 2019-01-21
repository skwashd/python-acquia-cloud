"""Test the AcquiaData class."""
import time
import unittest

import requests
import requests_mock

from acapi.resources.acquiadata import AcquiaData
from acapi.resources.task import Task


@requests_mock.Mocker()
class TestAcquiaData(unittest.TestCase):
    """Tests the AcquiaData class."""

    base_uri = 'http://example.com/api/'

    domain_uri = base_uri + 'sites/prod:example/envs/test/domains/example.com'

    def test_create_task(self, m):
        """Test create_task method."""
        task = {
            "completed": None,
            "created": int(time.time()),
            "description": "Dummy task",
            "id": 1234,
            "percentage": None,
            "queue": "test",
            "recipient": "server.example.com\n",
            "result": None,
            "sender": "cloud_api",
            "started": None,
            "state": "received"
        }

        adata = AcquiaData(self.domain_uri, None, {})
        atask = adata.create_task(self.domain_uri, task)

        self.assertIsInstance(atask, Task)

    def test_create_task_empty_string(self, m):
        """Test create_task method with empty string as task data."""
        adata = AcquiaData(self.domain_uri, None, {})
        with self.assertRaises(TypeError):
            adata.create_task(self.domain_uri, '')

    def test_create_task_empty_dict(self, m):
        """Test create_task method with invalid data."""
        adata = AcquiaData(self.domain_uri, None, {})
        with self.assertRaises(KeyError):
            adata.create_task(self.domain_uri, {})

    def test_get_404(self, m):
        """Tests a GET request that receives a 404 response."""

        uri = "{base_uri}{path}".format(base_uri=self.base_uri, path='invalid')

        m.register_uri('GET', uri + '.json', status_code=400)

        data = {}
        adata = AcquiaData(uri, None, data)

        with self.assertRaises(requests.exceptions.HTTPError):
            adata.request()

    def test_get_500s_retry(self, m):
        """Tests retrying a GET request that receives 50x response."""
        uri = "{base_uri}{path}".format(base_uri=self.base_uri, path='test')

        m.register_uri(
            'GET',
            "{uri}{ext}".format(uri=uri, ext=".json"),
            status_code=503
        )
        m.register_uri(
            'GET',
            "{uri}{ext}".format(uri=uri, ext=".json?acapi_retry=1"),
            status_code=504
        )
        m.register_uri(
            'GET',
            "{uri}{ext}".format(uri=uri, ext=".json?acapi_retry=2"),
            json={}
        )

        data = {}
        adata = AcquiaData(uri, None, data)

        response = adata.request()
        self.assertIsInstance(response, dict)

    def test_get_response_content(self, m):
        uri = "{domain}{ext}".format(domain=self.domain_uri, ext=".json")
        m.register_uri('GET', uri, status_code=200)

        adata = AcquiaData(self.domain_uri, None, {})
        response = adata.request(decode_json=False)
        self.assertIsInstance(response, bytes)


if __name__ == '__main__':
    unittest.main()
