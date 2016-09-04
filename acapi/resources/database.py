"""Database resource."""

import re

from acapi.resources.acquiaresource import AcquiaResource
from acapi.resources.backup import Backup
from acapi.resources.backuplist import BackupList


class Database(AcquiaResource):
    """Environment database."""

    #: Valid keys for environment object.
    valid_keys = ['db_cluster', 'host', 'instance_name', 'name', 'password',
                  'username']

    def backup(self, backup_id):
        """Fetch a backup.

        Parameters
        ----------
        backup_id : int
            The id of the database backup to fetch.

        Returns
        -------
        Backup
            The backup object.
        """
        uri = '{uri}/backups/{backup_id}'.format(uri=self.uri,
                                                 backup_id=backup_id)
        return Backup(uri, self.auth)

    def backups(self):
        """Fetch a list of database backups."""
        backups = BackupList(self.uri, self.auth)
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
        pattern = re.compile('/envs/(.*)/dbs/(.*)')
        matches = pattern.search(self.uri)
        current_env = matches.group(1)
        base_uri = pattern.sub(r'/dbs/\g<2>/db-copy/\g<1>', self.uri)

        copy_uri = '{uri}/{target}'.format(uri=base_uri, target=target)

        task_data = self.request(uri=copy_uri, method='POST')
        task = self.create_task(copy_uri, task_data)
        task.wait()

        # Another hack, this time to get the URI for the domain.
        env_search = '/{}/'.format(current_env)
        env_target = '/{}/'.format(target)
        new_uri = self.uri.replace(env_search, env_target)
        return Database(new_uri, self.auth)
