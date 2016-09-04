""" Acquia Cloud API data resource. """

import json
import logging
import requests
import requests_cache
import time

from acapi.version import __version__
from platform import python_version
from pprint import pformat

LOGGER = logging.getLogger('acapi.resources.acquiadata')


class AcquiaData(object):
    """Acquia Cloud API abstract network resource."""

    #: User Agent string
    RAW_AGENT = 'Acquia Cloud API Client/{mver} (Python {pver})'
    USER_AGENT = RAW_AGENT.format(mver=__version__,
                                  pver=python_version())

    def __init__(self, uri, auth, data=None):
        """Constructor.

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
        self.last_response = None

    def create_task(self, uri, data):
        """Create a new task object from a responses response object.

        Parameters
        ----------
        uri: str
            The URI for the action that triggered the task.
        data: dict
            The task data returned by the triggering request.

        Returns
        -------
        Task
            The Task object.
        """
        # We have to do this here to avoid circular dependencies
        from acapi.resources.task import Task
        task = Task(uri, self.auth, data=data)
        return task

    def get_last_response(self):
        """Fetch the last response object. """
        return self.last_response

    def request(self, uri=None, method='GET',
                data=None, params={}, decode_json=True):
        """Perform a HTTP requests.

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

        self.last_response = None

        if None == uri:
            uri = self.uri

        headers = {'User-Agent': self.USER_AGENT}

        uri = '{}.json'.format(uri)

        resp = None
        if 'GET' == method:
            attempt = 0
            while attempt <= 5:
                resp = requests.get(uri, auth=self.auth,
                                    headers=headers, params=params)

                if resp.status_code not in list(range(500, 505)):
                    # No need to retry for if not a server error type.
                    break

                attempt += 1
                params['acapi_retry'] = attempt
                time.sleep((attempt ** 2.0) / 10)

            # We need to unset the property or it sticks around.
            if 'acapi_retry' in params:
                del params['acapi_retry']

        if 'POST' == method:
            jdata = json.dumps(data)
            resp = requests.post(uri, auth=self.auth, headers=headers,
                                 params=params, data=jdata)
            # This is a sledgehammer but fine grained invalidation is messy.
            if self.is_cache_enabled():
                requests_cache.clear()

        if 'DELETE' == method:
            resp = requests.delete(uri, auth=self.auth, headers=headers,
                                   params=params)
            # Quickest and easiest way to do this.
            if self.is_cache_enabled():
                requests_cache.clear()

        if hasattr(resp, 'from_cache') and resp.from_cache:
            LOGGER.info("%s %s returned from cache", method, uri)

        self.last_response = resp

        if resp.status_code != requests.codes.ok:
            try:
                raise resp.raise_for_status()
            except requests.exceptions.HTTPError as exp:
                LOGGER.info("Failed request response headers: \n%s",
                            pformat(exp.response.headers, indent=2))
                raise

        if decode_json:
            return resp.json()

        return resp.content

    def is_cache_enabled(self):
        """Checks if requests cache is enabled.

        :return: Cache status.
        :rtype: bool.
        """
        return hasattr(requests.Session(), 'cache')
