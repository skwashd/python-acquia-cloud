"""Tests the backup class."""

import os
import sys
import tempfile

import requests_mock

from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestBackup(BaseTest):
    """Tests the Acquia Cloud API backup class."""

    backup = None

    def setUp(self):
        super(TestBackup, self).setUp()
        self.backup = self.client.site('mysite').environment('dev').db(
            'mysite').backup(22)

    def test_delete(self, mocker):
        """Test delte operation."""
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/dev/dbs/mysite/backups/22.json'

        mocker.register_uri(
            'DELETE',
            url,
            json=self.generate_task_dictionary(1117, 'waiting', False),
        )
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1117.json',
            json=self.generate_task_dictionary(1117, 'done', True),
        )
        self.assertTrue(self.backup.delete())

    def test_download_stream(self, mocker):
        """Test the download operation using stream."""
        if sys.version_info[0] < 3:
            text = "".join([
                r'0x1f', r'0x8b', r'0x08', r'0x08', r'0x7f', r'0x6e', r'0x80',
                r'0x56', r'0x00', r'0x03', r'0x74', r'0x65', r'0x73', r'0x74',
                r'0x2e', r'0x73', r'0x71', r'0x6c', r'0x00', r'0x03', r'0x00',
                r'0x00', r'0x00', r'0x00', r'0x00', r'0x00', r'0x00', r'0x00',
                r'0x00'
            ])
        else:
            text = str(bytes([
                0x1f, 0x8b, 0x08, 0x08, 0x7f, 0x6e, 0x80, 0x56, 0x00, 0x03,
                0x74, 0x65, 0x73, 0x74, 0x2e, 0x73, 0x71, 0x6c, 0x00, 0x03,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ]))

        backup = {
            "checksum": "042f31bebd595b6f2c84b3532d4f1a3b",
            "completed": "1331110381",
            "deleted": "0",
            "id": "22",
            "name": "mysite",
            "path": "backups/dev-mysite-mysitedev-2012-03-07.sql.gz",
            "started": "1331110381",
            "type": "daily",
            "link": "http://mysite.devcloud.acquia-sites.com/AH_DOWNLOAD?t=1342468716&prod=7386761671e68e517a74b7b790ef74d8a8fba7336dbc891cfef133bd29a7b238&d=/mnt/files/mysite.prod/backups/prod-mysite-mysite-2012-07-15.sql.gz"   # noqa: E501
        }
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/dev/dbs/mysite/backups/22.json'

        mocker.register_uri(
            'GET',
            url,
            json=backup
        )

        if sys.version_info[0] < 3:
            mocker.register_uri(
                'GET',
                'http://mysite.devcloud.acquia-sites.com/AH_DOWNLOAD?t=1342468716&prod=7386761671e68e517a74b7b790ef74d8a8fba7336dbc891cfef133bd29a7b238&d=/mnt/files/mysite.prod/backups/prod-mysite-mysite-2012-07-15.sql.gz',   # noqa: E501
                text=text,
                headers={"Content-Length": "116"}
            )
        else:
            mocker.register_uri(
                'GET',
                'http://mysite.devcloud.acquia-sites.com/AH_DOWNLOAD?t=1342468716&prod=7386761671e68e517a74b7b790ef74d8a8fba7336dbc891cfef133bd29a7b238&d=/mnt/files/mysite.prod/backups/prod-mysite-mysite-2012-07-15.sql.gz',    # noqa: E501
                text=text,
                headers={"Content-Length": "89"}
            )

        (handle, filename) = tempfile.mkstemp()
        self.assertTrue(self.backup.download(filename))
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
