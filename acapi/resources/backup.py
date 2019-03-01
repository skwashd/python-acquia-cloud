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

    valid_keys = [
        "completed",
        "created",
        "description",
        "id",
        "percentage",
        "queue",
        "recipient",
        "result",
        "sender",
        "started",
        "state",
    ]

    def delete(self):
        """Delete the current backup resource.

        Returns
        -------
        bool
            Was the backup deleted?

        """
        self.request(method="DELETE")
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
        url_parts = urlparse.urlparse(backup["link"])
        query = urlparse.parse_qs(url_parts.query)
        url_parts._replace(query="")
        uri = url_parts.geturl()

        bytes_total = bytes_read = 0  # needed for track if all content is read
        with open(target_file, "ab") as backup_file:
            while True:
                headers = {"Range": "bytes={}-".format(bytes_read)}
                response = self.request(
                    uri, headers=headers, params=query, decode_json=False, stream=True
                )

                if not bytes_total:
                    bytes_total = int(response.headers["Content-Length"])

                for chunk in response.iter_content(chunk_size=1024 * 36):
                    backup_file.write(chunk)

                bytes_read += response.raw.tell()

                if bytes_total == bytes_read:
                    break

        return True
