""" ACAPI base test class. """

import requests
import requests_mock
import unittest

from .. import Client

@requests_mock.Mocker()
class BaseTest(unittest.TestCase):
    """ Base test class for ACAPI. """

    # ACAPI Client
    client = None

    def setUp(self):
        """
        Set up the tests with the mock requests handler.
        """
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)

        self.client = Client('test', 'test', cache=None)

