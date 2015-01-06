""" Dictionary of Acquia Cloud API domain resources. """

from .acquialist import AcquiaList
from .domain import Domain
from .task import Task


class DomainList(AcquiaList):

    """ Dictionary of Acquia Cloud API domain resources. """

    def create(self, name):
        """Create a new domain object.

        name The FQDN to be created.

        return The new domain object.

        """
        uri = self.get_resource_uri(name)
        response = self.request(method='POST', uri=uri)
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Failed to create domain')

        domain = Domain(uri, self.auth)

        self.__setitem__(name, domain)

        return domain

    def get_resource_uri(self, fqdn):
        """ Generate the domain resource URI.

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
        """ Set the base URI for domain resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/domains'.format(base_uri)
        self.uri = uri
