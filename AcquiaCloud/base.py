import logging
import os
import platform

from six import integer_types, string_types, binary_type, iteritems
from .compat import urlparse, urlencode

from . import __version__
from .connection import Connection
from .imports import parse_qs, httplib2, json
from .util import transform_params, parse_rfc2822_date, UNSET_TIMEOUT


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

class Response(object):
    """
    Take a httplib2 response and turn it into a response object

    Borrowed from twilio-python.
    """
    def __init__(self, httplib_resp, content, url):
        self.headers = httplib_resp
        self.content = json.loads(content)
        self.cached = False
        self.status_code = int(httplib_resp.status)
        self.ok = self.status_code < 400
        self.url = url


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

