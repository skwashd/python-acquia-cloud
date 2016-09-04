"""Acquia Cloud API server list resource. """

from acapi.resources.acquialist import AcquiaList
from acapi.resources.server import Server


class ServerList(AcquiaList):
    """Dict of Acquia Cloud API Server resources keyed by hostname."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(ServerList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def fetch(self):
        """Fetch and store server objects. """
        servers = super(ServerList, self).request(uri=self.uri)
        for server in servers:
            name = str(server['name'])
            server_uri = self.get_resource_uri(name)
            self.__setitem__(name, Server(server_uri, self.auth, data=server))

    def get_resource_uri(self, name):
        """Generate the server URI.

        Parameters
        ----------
        name : str
            The hostname of the server.

        Returns
        -------
        str
            The server URI.
        """
        return '{base_uri}/{name}'.format(base_uri=self.uri, name=name)

    def set_base_uri(self, base_uri):
        """Set the base URI for server resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/servers'.format(base_uri)
        self.uri = uri
