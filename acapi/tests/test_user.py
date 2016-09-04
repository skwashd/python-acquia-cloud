"""Tests the Acquia Cloud API User class."""

import sys
import unittest

import requests_mock

from acapi import Client
from acapi.tests.basetest import BaseTest


@requests_mock.Mocker()
class TestUser(BaseTest):
    """Tests the Acquia Cloud API User class."""

    def test_drushrc(self, mocker):
        """Tests calling the drushrc() method."""
        json = {
            "mysite": {
                "dev": "$aliases['dev'] = array(...);",
                "test": "$aliases['test'] = array(...);"
            }
        }
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/me/drushrc.json',
            json=json
        )

        drushrc = self.client.user().drushrc()
        self.assertTrue('mysite' in drushrc.keys())

    @unittest.skipIf(sys.version_info >= (2, 8, 0),
                     "Recursive copy() call loop on 3.x")
    def test_user(self, mocker):
        """Tests fetching a user object."""
        email = 'user@example.com'
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/me.json',
            json={"authenticated_as": email}
        )
        client = Client(email, 'token')
        user = client.user()
        self.assertEqual(user['authenticated_as'], email)
