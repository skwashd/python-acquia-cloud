""" Acquia Cloud API Connection manager.

Lifted from twilio-python.
"""

from .imports import httplib2
from .imports import socks
from .imports import PROXY_TYPE_HTTP
from .imports import PROXY_TYPE_SOCKS4
from .imports import PROXY_TYPE_SOCKS5


class Connection(object):

    """Class for setting proxy configuration to be used for REST calls."""

    _proxy_info = None

    @classmethod
    def proxy_info(cls):
        """ Get the current proxy information.

        Returns
        -------
        httplib2.ProxyInfo
            The currently-set proxy information.
        """
        return cls._proxy_info

    @classmethod
    def set_proxy_info(cls, proxy_host, proxy_port,
                       proxy_type=PROXY_TYPE_HTTP, proxy_rdns=None,
                       proxy_user=None, proxy_pass=None):
        """Set proxy configuration for future REST API calls.

        Parameters
        ----------
        proxy_host : str
            Hostname of the proxy to use.
        proxy_port : int
            Port to connect to.
        proxy_type: str
            The proxy protocol to use. One of
            PROXY_TYPE_HTTP, PROXY_TYPE_SOCKS4, PROXY_TYPE_SOCKS5.
            Defaults to connection.PROXY_TYPE_HTTP.
        proxy_rdns : bool
            Use the proxy host's DNS resolver.
        proxy_user : str
            Username for the proxy.
        proxy_pass : str
            Password for the proxy.
        """
        cls._proxy_info = httplib2.ProxyInfo(
            proxy_type,
            proxy_host,
            proxy_port,
            proxy_rdns=proxy_rdns,
            proxy_user=proxy_user,
            proxy_pass=proxy_pass,
        )


_hush_pyflakes = [
    socks,
    PROXY_TYPE_SOCKS4,
    PROXY_TYPE_SOCKS5
]
