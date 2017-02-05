"""List of database backups."""

import json

from acapi.resources.acquialist import AcquiaList
from acapi.resources.backup import Backup


class BackupList(AcquiaList):
    """List of database backups for a site."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(BackupList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def create(self, timeout=3600):
        """Create a new backup."""
        task_data = self.request(method='POST')

        task = self.create_task(self.uri, task_data)
        task.wait(timeout)

        # For some reason Acquia encodes JSON as a string in a JSON object.
        result = json.loads(task['result'])
        backup_id = result['backupid']
        uri = '{uri}/{backup_id}'.format(uri=self.uri, backup_id=backup_id)
        backup = Backup(uri, self.auth)

        self.__setitem__(backup_id, backup)

        return backup

    def fetch(self):
        """Fetch and store database object."""
        backups = super(BackupList, self).request(uri=self.uri)
        for backup in backups:
            backup_id = int(backup['id'])
            uri = self.get_resource_uri(backup_id)
            self.__setitem__(backup_id, Backup(uri, self.auth, data=backup))

    def set_base_uri(self, base_uri):
        """Set the base URI for backup resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/backups'.format(base_uri)
        self.uri = uri
