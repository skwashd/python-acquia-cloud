""" Acquia Cloud API database list resource. """

import re
from .acquialist import AcquiaList
from .database import Database
from .task import Task


class DatabaseList(AcquiaList):

    """Dictionary of Acquia Cloud API database resources keyed by name."""

    def create(self, name):
        """ Creates a new database.

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
        response = self.request(method='POST', uri=uri, data={'db': name})
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Failed to create domain')

        db_uri = '{uri}/{name}'.format(uri=self.uri, name=name)
        db = Database(db_uri, self.auth)

        self.__setitem__(name, db)

        return db

    def get_resource_uri(self, name):
        """ Generate the database URI.

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
        """ Set the base URI for database resources.

        Parameters
        ----------
        base_uri : str
            The base URI to use for generating the new URI.
        """
        uri = '{}/dbs'.format(base_uri)
        self.uri = uri
