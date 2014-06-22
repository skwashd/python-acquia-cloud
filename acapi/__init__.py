import os

from .imports import httplib2, json
from .connection import Connection

from six import u

# Backwards compatibility.
from .version import __version__, __version_info__

from .util import make_acapi_request

from .resources import Site, User

def set_proxy_server(proxy_url, proxy_port):
    Connection.set_proxy_info(proxy_url, proxy_port)

class Client(object):
    '''
    A Client for accessing the Acquia Cloud API.

    :param str user: Acquia Cloud API username.

    :param str token: Acquia Cloud API user token.

    :param str realm: Acquia Cloud API realm (defaults to 'prod').

    :param str endpoint: Acquia Cloud API endpoint.
    '''

    def __init__(self, user=None, token=None, realm='prod', endpoint='https://cloudapi.acquia.com/v1'):
        '''
        Create an Acquia Cloud API REST client.
        '''
        if not user or not token:
            user, token = self.__find_credentials()
            if not user or not token:
                raise AcquiaCloudException("Credentials not provided")

        self.auth = (user, token)
        self.realm = realm
        self.endpoint = endpoint


    def generate_uri(self, path):
        uri = ('%s/%s' % (self.endpoint, path))
        return uri
    
    def site(self, name):
        namespace = ('sites/%s:%s' % (self.realm, name))
        uri = self.generate_uri(namespace)
        site = Site(uri, self.auth)
        return site

    def sites(self):
        sites = {}

        uri = self.generate_uri('sites')
        response = make_acapi_request('GET', uri, auth=self.auth)

        for site in response.content:
            realm, name = site.encode('ascii','ignore').split(':')
            site_uri = self.generate_uri('sites/%s' % (name))
            sites[name] = Site(site_uri, self.auth)

        return sites

    def user(self):
        """
        Returns the currently authenticated Cloud API user.
        """
        user = User(self.generate_uri('me'), self.auth)
        return user

    def __find_credentials(self):
        """
        Check environment variables for API credentials.
        """
        user = os.environ.get('ACQUIA_CLOUD_API_USER')
        token = os.environ.get('ACQUIA_CLOUD_API_TOKEN')
        return user, token

class AcquiaCloudException(Exception):
    pass

class AcquiaCloudRestException(AcquiaCloudException):
    """ A generic 400 or 500 level exception from the Acquia Cloud API

    This class was lifted from twilio-python and hacked.

    :param int status: the HTTP status that was returned for the exception
    :param str uri: The URI that caused the exception
    :param str msg: A human-readable message for the error
    :param str method: The HTTP method used to make the request
    """

    def __init__(self, status, uri, msg="", method='GET'):
        self.uri = uri
        self.status = status
        self.msg = msg
        self.method = method

    def __str__(self):
        subs = (self.method, self.uri, self.status, self.msg)
        return ('%s %s resulted in HTTP %s error: "%s"' % subs)



