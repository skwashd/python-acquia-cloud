"""Database Backup."""

import httplib2
from ..connection import Connection
from .acquiaresource import AcquiaResource


class Backup(AcquiaResource):

    """Acquia Cloud database backup."""

    def delete(self):
        """Delete the current backup resource.

        Returns
        -------
        bool
            Was the backup deleted?

        """
        response = self.request(method='DELETE')
        return response.ok

    def download(self, target_file):
        """Download a database backup from Acquia Cloud & write it to a file.

        Parameters
        ----------
        target_file : str
            The file to use for the backup. Overwrites file if it exists.

        Returns
        -------
        bool
            Was the backup retrieved and saved?

        """
        response = self.request()
        backup = response.content

        # We do this as acapi_request() assumes response is a json string.
        http = httplib2.Http(proxy_info=Connection.proxy_info())

        uri = backup['link'].encode('ascii', 'ignore')
        resp, content = http.request(uri, 'GET')

        file = open(target_file, 'wb')
        file.write(content)
        file.close()

        return True
