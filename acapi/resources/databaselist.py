""" Acquia Cloud API database list resource. """

import re

from acapi.resources.acquialist import AcquiaList
from acapi.resources.database import Database


class DatabaseList(AcquiaList):
    """Dictionary of Acquia Cloud API database resources keyed by name."""

    def __init__(self, base_uri, auth, *args, **kwargs):
        """Constructor."""
        super(DatabaseList, self).__init__(base_uri, auth, *args, **kwargs)
        self.fetch()

    def create(self, name):
        """Create a new database.

        Parameters
        ----------
        name: str
            The name of the new database.

        Returns
        -------
        Database
            The new database object.
        """
        base_uri = re.sub(r'/envs/(.+)/dbs', '', self.uri)
        uri = '{base_uri}/dbs'.format(base_uri=base_uri)

        task_data = self.request(method='POST', uri=uri, data={'db': name})
        task = self.create_task(uri, task_data)
        task.wait()

        db_uri = '{uri}/{name}'.format(uri=self.uri, name=name)
        db_obj = Database(db_uri, self.auth)

        self.__setitem__(name, db_obj)

        return db_obj

    def fetch(self):
        """Fetch and store database objects. """
        dbs = super(DatabaseList, self).request(uri=self.uri)
        for db_obj in dbs:
            name = str(db_obj['name'])
            db_uri = self.get_resource_uri(name)
            self.__setitem__(name, Database(db_uri, self.auth, data=db_obj))

    def get_resource_uri(self, name):
        """Generate the database URI.

        Parameters
        ----------
        name : str
            The name of the database.

        Returns
        -------
        str
            The database URI.
        """
        return '{base_uri}/{name}'.format(base_uri=self.uri, name=name)

    def set_base_uri(self, base_uri):
        """Set the base URI for database resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/dbs'.format(base_uri)
        self.uri = uri
