"""Database Backup."""

try:
    # Backwards compatible Python 3
    import urllib.parse as urlparse
except ImportError:
    # Python 2.x
    import urlparse

from acapi.resources.acquiaresource import AcquiaResource


class Backup(AcquiaResource):
    """Acquia Cloud database backup."""

    valid_keys = ['completed', 'created', 'description', 'id', 'percentage',
                  'queue', 'recipient', 'result', 'sender', 'started', 'state']

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

        # Hack to make the download URL work for requests
        url_parts = urlparse.urlparse(backup['link'])
        query = urlparse.parse_qs(url_parts.query)
        url_parts._replace(query='')
        uri = url_parts.geturl()

        content = self.request(uri=uri, params=query, decode_json=False)

        backup_file = open(target_file, 'wb')
        backup_file.write(content)
        backup_file.close()

        return True
