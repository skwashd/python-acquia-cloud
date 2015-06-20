"""Utility functions.

Functions lifted from twilio-python's util.py and base.py as noted.

"""

import datetime
import logging
import os
import platform

from email.utils import parsedate
from six import integer_types, string_types, binary_type, iteritems

from .version import __version__
from .compat import urlparse, urlencode
from .connection import Connection
from .imports import parse_qs, httplib2, json
from .exceptions import AcquiaCloudException, AcquiaCloudRestException
from .response import Response


def make_request(method, url, params=None, data=None, headers=None,
                 cookies=None, files=None, auth=None, timeout=None,
                 allow_redirects=False, proxies=None):
    """Send a HTTP request.

    Hacked up version of twilio-python function of the same name.

    Currently proxies, files, and cookies are all ignored.

    Parameters
    ----------
    method : str
        The HTTP method to use.
    url : str
        The URL to request.
    params : dict
        Query parameters to append to the URL.
    data : dict
        Parameters to go in the body of the HTTP request.
    headers : dict
        HTTP Headers to send with the request.
    timeout : float
        Socket/Read timeout for the request.

    Returns
    -------
    Response
        A HTTP response object.
    """
    http = httplib2.Http(
        timeout=timeout,
        proxy_info=Connection.proxy_info(),
    )
    http.follow_redirects = allow_redirects

    if auth is not None:
        http.add_credentials(auth[0], auth[1])

    if data is not None:
        data = json.dumps(data)

    if params is not None:
        enc_params = urlencode(params, doseq=True)
        if urlparse(url).query:
            url = '%s&%s' % (url, enc_params)
        else:
            url = '%s?%s' % (url, enc_params)

    resp, content = http.request(url, method, headers=headers, body=data)
    logging.info('Requested %s %s Response: %s (%s)', method, url, resp.reason, resp.status)

    # Format httplib2 request as requests object
    return Response(resp, content.decode('utf-8'), url)


def acapi_request(method, uri, **kwargs):
    """Make a request to Acquia Cloud API. Throws an error.

    Modified version of make_twilio_request function in twilio-python.

    :return: a requests-like HTTP response
    :rtype: :class:`RequestsResponse`
    :raises AcquiaCloudRestException: if the response is a 400
        or 500-level response.

    """
    headers = kwargs.get("headers", {})

    user_agent = "Acquia Cloud API/%s (Python %s)" % (
        __version__,
        platform.python_version(),
    )
    headers["User-Agent"] = user_agent
    # Acquia Cloud API only supports UTF-8 json.
    headers["Accept-Charset"] = "utf-8"
    headers["Accept"] = "application/json"
    uri += ".json"

    if method == "POST" and "Content-Type" not in headers:
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    kwargs["headers"] = headers

    resp = make_request(method, uri, **kwargs)

    if not resp.ok:
        try:
            error = json.loads(resp.content)
            code = error["code"]
            message = "%s: %s" % (code, error["message"])
        except:
            code = None
            message = resp.content

        raise AcquiaCloudRestException(status=resp.status_code, method=method,
                                       uri=resp.url, msg=message)

    return resp


class _UnsetTimeoutKls(object):

    """A sentinel for an unset timeout.

    Defaults to the system timeout.

    """

    def __repr__(self):
        return '<Unset Timeout Value>'


# None has special meaning for timeouts, so we use this sigil to indicate
# that we don't care
UNSET_TIMEOUT = _UnsetTimeoutKls()
