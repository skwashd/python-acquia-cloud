"""Dictionary of Acquia Cloud API site resources. """

from acapi.resources.acquialist import AcquiaList
from acapi.resources.site import Site


class SiteList(AcquiaList):
    """Dictionary of site resources."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(SiteList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def fetch(self):
        """Fetch and store site objects."""
        sites = super(SiteList, self).request(uri=self.uri)
        for site in sites:
            realm, name = str(site).split(':')
            site_uri = self.get_resource_uri(name, realm=realm)
            self.__setitem__(name, Site(site_uri, self.auth))

    def get_resource_uri(self, name, realm='prod'):
        """Generate the server URI.

        Parameters
        ----------
        name : str
            The subscription name of the site.

        Returns
        -------
        str
            The site URI.
        """
        return '{base_uri}/{realm}:{name}'.format(base_uri=self.uri,
                                                  realm=realm, name=name)

    def set_base_uri(self, base_uri):
        """Set the base URI for site resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/sites'.format(base_uri)
        self.uri = uri
