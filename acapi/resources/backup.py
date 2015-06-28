"""Database Backup."""

from .acquiaresource import AcquiaResource

class Backup(AcquiaResource):

    """Acquia Cloud database backup."""

    valid_keys = ['completed', 'created', 'description', 'id', 'percentage', 'queue',
                  'recipient', 'result', 'sender', 'started', 'state']

    def delete(self):
        """Delete the current backup resource.

        Returns
        -------
        bool
            Was the backup deleted?

        """
        self.request(method='DELETE')
        return True

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
        backup = response

        uri = backup['link'].encode('ascii', 'ignore')
        content = self.request(uri=uri, decode_json=False)

        backup_file = open(target_file, 'wb')
        backup_file.write(content)
        backup_file.close()

        return True
