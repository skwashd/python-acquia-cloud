"""
Utility functions

Functions lifted from twilio-python's util.py and base.py as noted.
"""

import datetime
import os
import platform

from email.utils import parsedate
from six import integer_types, string_types, binary_type, iteritems

from . import __version__
from .compat import urlparse, urlencode
from .connection import Connection
from .imports import parse_qs, httplib2, json
from .exceptions import AcquiaCloudException, AcquiaCloudRestException
from .response import Response

def make_request(method, url, params=None, data=None, headers=None,
                 cookies=None, files=None, auth=None, timeout=None,
                 allow_redirects=False, proxies=None):
    """Sends an HTTP request

    Hacked up version of twilio-python function of the same name.

    :param str method: The HTTP method to use
    :param str url: The URL to request
    :param dict params: Query parameters to append to the URL
    :param dict data: Parameters to go in the body of the HTTP request
    :param dict headers: HTTP Headers to send with the request
    :param float timeout: Socket/Read timeout for the request

    :return: An http response
    :rtype: A :class:`Response <models.Response>` object

    See the requests documentation for explanation of all these parameters

    Currently proxies, files, and cookies are all ignored
    """
    http = httplib2.Http(
        timeout=timeout,
        proxy_info=Connection.proxy_info(),
    )
    http.follow_redirects = allow_redirects

    if auth is not None:
        http.add_credentials(auth[0], auth[1])

    def encode_atom(atom):
            if isinstance(atom, (integer_types, binary_type)):
                return atom
            elif isinstance(atom, string_types):
                return atom.encode('utf-8')
            else:
                raise ValueError('list elements should be an integer, '
                                 'binary, or string')

    if data is not None:
        data = json.dumps(data)

    if params is not None:
        enc_params = urlencode(params, doseq=True)
        if urlparse(url).query:
            url = '%s&%s' % (url, enc_params)
        else:
            url = '%s?%s' % (url, enc_params)

    resp, content = http.request(url, method, headers=headers, body=data)

    # Format httplib2 request as requests object
    return Response(resp, content.decode('utf-8'), url)


def make_acapi_request(method, uri, **kwargs):
    """
    Make a request to Acquia Cloud API. Throws an error

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


def parse_date(d):
    """
    Return a string representation of a date that the Twilio API understands
    Format is YYYY-MM-DD. Returns None if d is not a string, datetime, or date
    """
    if isinstance(d, datetime.datetime):
        return str(d.date())
    elif isinstance(d, datetime.date):
        return str(d)
    elif isinstance(d, str):
        return d


def parse_rfc2822_date(s):
    """
    Parses an RFC 2822 date string and returns a time zone naive datetime
    object. All dates returned from Twilio are UTC.
    """
    date_tuple = parsedate(s)
    if date_tuple is None:
        return None
    return datetime.datetime(*date_tuple[:6])


def convert_case(s):
    """
    Given a string in snake case, convert to CamelCase

    Ex:
    date_created -> DateCreated
    """
    return ''.join([a.title() for a in s.split("_") if a])


class _UnsetTimeoutKls(object):
    """ A sentinel for an unset timeout. Defaults to the system timeout. """
    def __repr__(self):
        return '<Unset Timeout Value>'


# None has special meaning for timeouts, so we use this sigil to indicate
# that we don't care
UNSET_TIMEOUT = _UnsetTimeoutKls()
