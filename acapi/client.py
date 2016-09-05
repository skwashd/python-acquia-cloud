""" Acquia Cloud API client. """

import os
import requests_cache

import acapi.exceptions
from acapi.resources.site import Site
from acapi.resources.sitelist import SiteList
from acapi.resources.user import User


class Client(object):
    """A Client for accessing the Acquia Cloud API."""

    def __init__(
            self, user=None, token=None, realm='prod',
            endpoint='https://cloudapi.acquia.com/v1',
            cache=600):
        """Create an Acquia Cloud API REST client.

        Parameters
        ----------
        user : str
            Acquia Cloud API username.
        token : str
            Acquia Cloud API user token.
        realm : str
            Acquia Cloud API realm (defaults to 'prod').
        endpoint : str
            Base Acquia Cloud API endpoint URL.
        cache: int
            How long API responses should be cached for.

        """
        if not user or not token:
            user, token = self.__find_credentials()
            if not user or not token:
                msg = "Credentials not provided"
                raise acapi.exceptions.AcquiaCloudException(msg)

        self.auth = (user, token)
        self.realm = realm
        self.endpoint = endpoint

        if cache is not None:
            requests_cache.install_cache(cache_name='acapi',
                                         backend='memory',
                                         expire_after=cache)

    def generate_uri(self, path):
        """Generate a URI for a ACAPI request.

        Parameters
        ----------
        path : str
            The path component of the URI

        Returns
        -------
        str
            The generates URI.

        """
        uri = '{endpoint}/{path}'.format(endpoint=self.endpoint, path=path)
        return uri

    def site(self, name):
        """Retrieve a site object.

        Parameters
        ----------
        name : str
            The Acquia site/subscription name to look up.

        Returns
        -------
        Site
            The site object.

        """
        namespace = ('sites/%s:%s' % (self.realm, name))
        uri = self.generate_uri(namespace)
        site = Site(uri, self.auth)
        return site

    def sites(self):
        """Retrieve a list of available sites.

        Returns
        -------
        SiteList
            dict of sites keyed by site name.

        """
        sites = SiteList(self.endpoint, self.auth)
        return sites

    def user(self):
        """Retrieve the currently authenticated Cloud API user."""
        user = User(self.generate_uri('me'), self.auth)
        return user

    def __find_credentials(self):
        """Check environment variables for API credentials."""
        user = os.environ.get('ACQUIA_CLOUD_API_USER')
        token = os.environ.get('ACQUIA_CLOUD_API_TOKEN')
        return user, token
