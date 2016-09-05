"""Dictionary of Acquia Cloud API task resources."""

from acapi.resources.acquialist import AcquiaList
from acapi.resources.task import Task


class TaskList(AcquiaList):
    """Dictionary of task resources."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(TaskList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def fetch(self):
        """Fetch and store task objects. """
        tasks = super(TaskList, self).request(uri=self.uri)
        for task in tasks:
            task_id = int(task['id'])
            task_uri = self.get_resource_uri(task_id)
            self.__setitem__(task_id, Task(task_uri, self.auth, data=task))

    def set_base_uri(self, base_uri):
        """Set the base URI for task resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/tasks'.format(base_uri)
        self.uri = uri
