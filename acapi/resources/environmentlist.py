"""Acquia Cloud API server list resource."""

from acapi.resources.acquialist import AcquiaList
from acapi.resources.environment import Environment


class EnvironmentList(AcquiaList):
    """Dict of Acquia Cloud API Environment resources keyed by short name."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(EnvironmentList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def fetch(self):
        """Fetch and store environment objects."""
        envs = super(EnvironmentList, self).request(uri=self.uri)
        for env in envs:
            name = str(env['name'])
            env_uri = self.get_resource_uri(name)
            self.__setitem__(name, Environment(env_uri, self.auth, data=env))

    def get_resource_uri(self, name):
        """Generate the resource URI.

        Parameters
        ----------
        name : str
            The name of the environment resource.

        Returns
        -------
        str
            The resource URI.
        """
        return '{base_uri}/{name}'.format(base_uri=self.uri, name=name)

    def set_base_uri(self, base_uri):
        """Set the base URI for server resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/envs'.format(base_uri)
        self.uri = uri
