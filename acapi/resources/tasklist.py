""" Dictionary of Acquia Cloud API task resources. """

from .acquialist import AcquiaList
from .task import Task


class TaskList(AcquiaList):

    """ Dictionary of task resources. """

    def set_base_uri(self, base_uri):
        """ Set the base URI for task resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/tasks'.format(base_uri)
        self.uri = uri
