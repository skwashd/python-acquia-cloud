"""Dictionary of Acquia Cloud API domain resources. """

from acapi.resources.acquialist import AcquiaList
from acapi.resources.domain import Domain


class DomainList(AcquiaList):
    """Dictionary of Acquia Cloud API domain resources."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(DomainList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def create(self, name):
        """Create a new domain object.

        name The FQDN to be created.

        return The new domain object.

        """
        uri = self.get_resource_uri(name)
        task_data = self.request(uri=uri, method='POST')
        task = self.create_task(uri, task_data)
        task.wait()

        domain = Domain(uri, self.auth)

        self.__setitem__(name, domain)

        return domain

    def fetch(self):
        """Fetch and store domain objects."""
        domains = super(DomainList, self).request(uri=self.uri)
        for domain in domains:
            name = str(domain['name'])
            domain_uri = self.get_resource_uri(name)
            self.__setitem__(name, Domain(domain_uri, self.auth, data=domain))

    def get_resource_uri(self, fqdn):
        """Generate the domain resource URI.

        Parameters
        ----------
        fqdn : str
            The FDQN of the domain resource.

        Returns
        -------
        str
            The server URI.
        """
        return '{base_uri}/{fqdn}'.format(base_uri=self.uri, fqdn=fqdn)

    def set_base_uri(self, base_uri):
        """Set the base URI for domain resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/domains'.format(base_uri)
        self.uri = uri
