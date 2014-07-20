""" Acquia Cloud API database list resource. """

from .acquialist import AcquiaList


class DatabaseList(AcquiaList):

    """Dictionary of Acquia Cloud API database resources keyed by name."""

    def get_resource_uri(self, name):
        """ Generate the database URI.

        Parameters
        ----------
        name : str
            The name of the database.

        Returns
        -------
        str
            The database URI.
        """
        return '{base_uri}/{name}'.format(base_uri=self.uri, name=name)

    def set_base_uri(self, base_uri):
        """ Set the base URI for database resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/dbs'.format(base_uri)
        self.uri = uri
