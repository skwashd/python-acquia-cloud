""" Database resource. """

import re
from .acquiaresource import AcquiaResource
from .backup import Backup
from .backuplist import BackupList
from .task import Task


class Database(AcquiaResource):

    """Environment database."""

    def backup(self, id):
        """Fetch a backup.

        Parameters
        ----------
        id : int
            The id of the database backup to fetch.

        Returns
        -------
        Backup
            The backup object.
        """
        uri = '{uri}/backups/{id}'.format(uri=self.uri, id=id)
        return Backup(uri, self.auth)

    def backups(self):
        """Fetch a list of database backups."""
        backups = BackupList(self.uri, self.auth)

        response = self.request(uri=backups.uri)
        for backup in response.content:
            id = int(backup['id'])
            backup_uri = backups.get_resource_uri(id=id)
            backups[id] = Backup(backup_uri, self.auth, data=backup)

        return backups

    def copy(self, target):
        """Copy a database to another environment.

        Parameters
        ----------
        target : string
            Name of the target environment.

        Returns
        -------
        Database
            Target database object.
        """
        # More regex hacks to work around the limitations of the ACAPI.
        p = re.compile('/envs/(.*)/dbs/(.*)')
        m = p.search(self.uri)
        current_env = m.group(1)
        db = m.group(2)
        base_uri = p.sub('/dbs/\g<2>/db-copy/\g<1>', self.uri)

        copy_uri = '{uri}/{target}'.format(uri=base_uri, target=target)

        response = self.request(uri=copy_uri, method='POST')
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Unable to request backup')

        # Another hack, this time to get the URI for the domain.
        env_search = '/{}/'.format(current_env)
        env_target = '/{}/'.format(target)
        new_uri = self.uri.replace(env_search, env_target)
        return Database(new_uri, self.auth)
