"""Tests the Acquia Cloud API Client class."""

import os

import requests_mock

from acapi import Client
from acapi.exceptions import AcquiaCloudException
from acapi.resources.site import Site
from acapi.resources.sitelist import SiteList
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestClient(BaseTest):
    """Tests the Acquia Cloud API client class."""

    def test_find_credentials(self, mocker):
        """Tests finding the credentials in environment variables."""
        os.environ["ACQUIA_CLOUD_API_USER"] = "user"
        os.environ["ACQUIA_CLOUD_API_TOKEN"] = "token"
        client = Client(cache=None)
        (user, token) = client._Client__find_credentials()
        self.assertEqual(user, "user")
        self.assertEqual(token, "token")

    def test_find_credentials_none_set(self, mocker):
        """Tests finding empty credentials in environment variables."""

        os.environ["ACQUIA_CLOUD_API_USER"] = ""
        os.environ["ACQUIA_CLOUD_API_TOKEN"] = ""
        with self.assertRaises(AcquiaCloudException) as context:
            Client(cache=None)

        self.assertEqual(str(context.exception), "Credentials not provided")

    def test_site(self, mocker):
        """Tests calling the site() method."""

        site_name = "mysite"
        json = {
            "title": "My Site",
            "name": site_name,
            "production_mode": "0",
            "unix_username": "mysite",
            "vcs_type": "git",
            "vcs_url": "mysite@svn-3.bjaspan.hosting.acquia.com:mysite.git",
        }

        mocker.register_uri(
            "GET",
            "https://cloudapi.acquia.com/v1/site/prod:{}.json".format(site_name),
            json=json,
        )

        site = self.client.site(site_name)
        self.assertIsInstance(site, Site)

    def test_sites(self, mocker):
        """Tests calling the sites() method."""
        site_name = "mysite"

        mocker.register_uri(
            "GET",
            "https://cloudapi.acquia.com/v1/sites.json",
            json=["prod:{}".format(site_name)],
        )

        sites = self.client.sites()
        self.assertIsInstance(sites, SiteList)
