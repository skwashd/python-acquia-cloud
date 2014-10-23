""" Acquia Cloud API server list resource. """

from .acquialist import AcquiaList


class EnvironmentList(AcquiaList):

    """Dict of Acquia Cloud API Server resources keyed by hostname."""

    def get_resource_uri(self, name):
        """ Generate the resource URI.

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
        """ Set the base URI for server resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/envs'.format(base_uri)
        self.uri = uri
