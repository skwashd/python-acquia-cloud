""" Acquia Cloud API data resource. """

import re
import time

from ..util import acapi_request


class AcquiaData(object):

    """Acquia Cloud API abstract network resource."""

    def __init__(self, uri, auth, data=None):
        """ Constructor.

        Parameters
        ----------
        uri : str
            The base URI for the resource.
        auth : tuple
             The authentication credentials to use for the request.
        data : dict
            Raw data from ACAPI.
        """
        self.uri = uri
        self.auth = auth
        self.data = data

    def request(self, uri=None, method='GET', data=None, params=None):
        """Helper function for requesting resources.

        Parameters
        ----------
        uri : str
            The URI to use for the request.
        method : str
            The HTTP method to use for the request.
        auth : tuple
            The authentication credentials to use for the request.
        data : dict
            Any data to send as part of a post request body.
        params : dict
            Query string parameters.

        Returns
        -------
        dict
            Decoded JSON response data as a dict object.
        """
        if None == uri:
            uri = self.uri

        return acapi_request(method, uri, auth=self.auth,
                             data=data, params=params)
