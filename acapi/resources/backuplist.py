""" List of database backups. """

import json
from .acquialist import AcquiaList
from .backup import Backup
from .task import Task


class BackupList(AcquiaList):

    """List of database backups for a site."""

    def create(self):
        """Create a new backup."""
        response = self.request(method='POST')
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Unable to request backup')

        id = int(json.loads(task['result'])['backupid'])
        uri = '{uri}/{id}'.format(uri=self.uri, id=id)
        backup = Backup(uri, self.auth)

        self.__setitem__(id, backup)

        return backup

    def set_base_uri(self, base_uri):
        """ Set the base URI for backup resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/backups'.format(base_uri)
        self.uri = uri
