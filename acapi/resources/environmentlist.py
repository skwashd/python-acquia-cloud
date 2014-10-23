""" Acquia Cloud API server list resource. """

from .acquialist import AcquiaList


class EnvironmentList(AcquiaList):

    """Dict of Acquia Cloud API Server resources keyed by hostname."""

    def set_base_uri(self, base_uri):
        """ Set the base URI for server resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/envs'.format(base_uri)
        self.uri = uri
