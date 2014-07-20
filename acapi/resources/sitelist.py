""" Dictionary of Acquia Cloud API site resources. """

from .acquialist import AcquiaList


class SiteList(AcquiaList):

    """ Dictionary of site resources. """

    def get_resource_uri(self, name, realm='prod'):
        """ Generate the server URI.

        Parameters
        ----------
        name : str
            The subscription name of the site.

        Returns
        -------
        str
            The site URI.
        """
        return '{base_uri}/{realm}:{name}'.format(
                                                  base_uri=self.uri,
                                                  realm=realm,
                                                  name=name)

    def set_base_uri(self, base_uri):
        """ Set the base URI for site resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/sites'.format(base_uri)
        self.uri = uri
